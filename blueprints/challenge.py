import time
import unittest
from typing import Any, List, Dict, Tuple, Optional


from flask import Blueprint, render_template, flash, jsonify, request, Request, session
#from RestrictedPython import compile_restricted, safe_globals
#from RestrictedPython.Eval import default_guarded_getiter
#from RestrictedPython.Guards import guarded_iter_unpack_sequence


from challenges import get_challenges, R2Challenge, save_challenge
from submissions import get_submissions_by_challenge_id, save_submission, Submission


bp = Blueprint('challenge', __name__)


def generate_safest_globals() -> Dict[str, Any]:
	testing_globals = {
		**safe_globals,
		'unittest': unittest
	}
	testing_globals.setdefault('__builtins__', {}).update({
		'__metaclass__': type,
		'_getiter_': default_guarded_getiter,
		'_iter_unlock_sequence': guarded_iter_unpack_sequence,
		'unittest': unittest
	})
	return testing_globals

def generate_safest_globals():
	return { 'unittest': unittest }



class R2TestResult(unittest.TestResult):
	def __init__(self, *args: Any, **kwargs: Any):
		super().__init__(*args, **kwargs)
		self.successful: List[unittest.TestCase] = []

	def addSuccess(self, test: unittest.TestCase):
		self.successful.append(test)


def run_challenge_code(challenge: R2Challenge, code: str) -> Tuple[bool, str]:
	test_locals = {'unittest': unittest}
	# handle bad code - syntax error, etc
	exec(
		#compile_restricted(code, '<inline>', 'exec'),
		compile(code, '<inline>', 'exec'),
		generate_safest_globals(),
		test_locals
	)
	test_code, test_class_name = challenge['testing_code']
	exported_code_name = challenge['template_code'][1]
	exec(
		test_code,
		{
			**generate_safest_globals(),
			'__name__': 'r2_testing_code',
			exported_code_name: test_locals[exported_code_name]
		},
		test_locals
	)
	results: R2TestResult = unittest.TextTestRunner(resultclass=R2TestResult).run(
		unittest.defaultTestLoader.loadTestsFromTestCase(test_locals[test_class_name])
	) # type: ignore
	full_output = ''

	if results.successful:
		full_output += f'{len(results.successful)} tests passed\n\n'
	# TODO - handle unexpected successes
	# TODO - seperate output for each test that is not hidden

	failed = results.failures + results.errors
	hidden = 0
	for test, output in failed:
		if test._testMethodName in getattr(test, 'HIDDEN_TESTS', []):
			hidden += 1
			continue
		full_output += output + '\n'

	if hidden:
		full_output += f'{hidden} hidden test cases failed'

	return results.testsRun == len(results.successful), full_output.strip()

def get_challenge_and_user_code(request: Request) -> Tuple[Optional[R2Challenge], str]:
	# TODO - handle invalid challenge id
	challenge_id = float(request.form['id'])
	# todo - handle challenge not found
	challenge = next((challenge for challenge in get_challenges() if challenge['id'] == challenge_id), None)
	code: str = request.form.get('code', '')
	return challenge, code


@bp.route('/c/<challenge_id>')
def challenge(challenge_id: str):
	try:
		challenge_id = float(challenge_id)
	except:
		flash(f'Challenge "{challenge_id}" not found')
		return render_template('pages/404.j2'), 404

	challenge = next((
		challenge
		for challenge in get_challenges()
		if challenge['id'] == challenge_id
	), None)
	if not challenge:
		flash(f'Challenge "{challenge_id}" not found')
		return render_template('pages/404.j2'), 404

	submissions = []
	user_submission = None
	username = session.get('user', {'username': session['id']})['username']
	submissions = get_submissions_by_challenge_id(challenge_id)
	user_submission = next((submission for submission in submissions if submission['author'] == username), None)
	if user_submission:
		submissions.remove(user_submission)

	return render_template(
		'pages/challenge.j2',
		challenge=challenge,
		submissions=submissions,
		user_submission=user_submission
	)

@bp.route('/api/run', methods=['POST'])
def run():
	challenge, code = get_challenge_and_user_code(request)
	success, output = run_challenge_code(challenge, code)
	return jsonify({ 'success': success, 'output': output })

@bp.route('/api/submit', methods=['POST'])
def submit():
	challenge, code = get_challenge_and_user_code(request)
	assert challenge
	success, output = run_challenge_code(challenge, code)
	if success:
		save_submission(Submission(
			when=time.time(),
			challenge_id=challenge['id'],
			author=session.get('user', {'username': session['id']})['username'],
			code=code
		))

	return jsonify({ 'success': success, 'output': output })


@bp.route('/create')
def create():
	return render_template('pages/create.j2')

@bp.route('/api/create_challenge', methods=['POST'])
def create_challenge():
	working_code = request.form['working_code']

	challenge = R2Challenge(
		id=time.time(),
		title=request.form['title'],
		description=request.form['description'],
		hints=[],
		template_code=(request.form['template_code'], request.form['template_code_export']),
		testing_code=(request.form['test_code'], request.form['test_code_export']),
	)
	success, output = run_challenge_code(challenge, working_code)

	if not success:
		return jsonify({ 'success': False, 'output': output })

	save_challenge(challenge)

	return jsonify({ 'success': True, 'id': challenge['id']})