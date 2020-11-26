from typing import TypedDict, List, Optional

from replit import db


Submission = TypedDict('Submission', {
	'when': float,
	'challenge_id': float,
	'author': Optional[str],
	'code': str
})


def get_submissions_by_username(username: str, submissions=None) -> List[Submission]:
	if not submissions:
		submissions = get_submissions()

	return [
		submission
		for submission in submissions
		if (submission['author'] or '').lower() == username.lower()
	]

def get_submissions_by_challenge_id(challenge_id: float) -> List[Submission]:
	return [
		submission
		for submission in get_submissions()
		if submission['challenge_id'] == challenge_id
	]

def get_submissions() -> List[Submission]:
	subs = []
	for key in db.prefix('submission_'):
		subs.append(db[key])
	return subs

def save_submission(submission: Submission):
	db[f'submission_{submission["when"]}'] = submission