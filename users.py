from typing import TypedDict, Dict, List, Optional


from replit import db

User = TypedDict('User', {
	'username': str,
	'password': str,
	'joined': float
})

def get_user_by_username(username: str) -> Optional[User]:
	return next((user for user in get_users() if username.lower() == user['username'].lower()), None)

def _get_user_dict() -> Dict[str, User]:
	dct = {}
	for key in db.prefix('user_'):
		user = db[key]
		dct[user['username']] = user
	return dct		

def get_users() -> List[User]:
	return list(_get_user_dict().values())

def save_user(user: User):
	db[f'users_{user["username"]}'] = user
