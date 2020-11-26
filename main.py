import os
import time


from flask import Flask, render_template, session


from challenges import get_challenges
from submissions import get_submissions, get_submissions_by_username
from blueprints.challenge import bp as challenge_bp
from blueprints.auth import bp as auth_bp


app = Flask('app')
# TODO - only enable outside of production
#app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = 'super secret key'
app.register_blueprint(challenge_bp)
app.register_blueprint(auth_bp)

@app.route('/')
def home():
	if 'id' not in session:
		session['id'] = str(time.time())
	challenges = get_challenges()

	username = session.get('user', {'username': session['id']})['username']
	submissions = get_submissions()
	user_submissions = get_submissions_by_username(username, submissions)

	completed_map = {}
	challenge_map = {challenge['id']: challenge for challenge in challenges}
	for submission in user_submissions:
		challenge_id = submission['challenge_id']
		completed_map[challenge_id] = challenge_map[challenge_id]
		del challenge_map[challenge_id]
	next_challenge = challenge_map[sorted(challenge_map.keys())[0]] if challenge_map else None

	latest_submissions = sorted(submissions, key=lambda submission: submission['when'], reverse=True)
	for submission in latest_submissions[:]:
		if submission['challenge_id'] not in completed_map:
			latest_submissions.remove(submission)

	return render_template(
		'pages/home.j2',
		challenge=next_challenge,
		completed_challenges=list(completed_map.values()),
		uncompleted_challenges=list(challenge_map.values()),
		latest_submissions=latest_submissions
	)


app.run(host='0.0.0.0', port=os.getenv('PORT', 8081))