from submissions import get_submissions_by_username
import time


from flask import Blueprint, render_template, flash, request, session, redirect, url_for
import bcrypt


from users import get_user_by_username, save_user, User


bp = Blueprint('auth', __name__)

@bp.route('/u/<username>')
def user_page(username: str):
	user = get_user_by_username(username)
	if not user:
		flash(f'User "{username}" not found')
		return render_template('pages/404.j2'), 404

	return render_template(
		'pages/user.j2',
		user=user,
		submissions=get_submissions_by_username(user['username'])
	)

@bp.route('/auth')
def auth():
	return render_template('pages/auth.j2')


@bp.route('/logout')
def logout():
	if 'user' in session:
		del session['user']

	return redirect(url_for('home'))


@bp.route('/api/signup', methods=['POST'])
def signup():
	username: str = request.form['username']

	if get_user_by_username(username):
		flash('User already exists')
		return redirect(url_for('.auth'))

	password: str = request.form['password']
	hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

	user = User(username=username, password=hashed.decode(), joined=time.time())
	session['user'] = user
	save_user(user)

	flash('Successfully signed up')
	return redirect(url_for('home'))


@bp.route('/api/login', methods=['POST'])
def login():
	username: str = request.form['username']

	user = get_user_by_username(username)
	if not user or not bcrypt.checkpw(request.form['password'].encode(), user['password'].encode()):
		flash('Invalid credentials')
		return redirect(url_for('.auth'))

	session['user'] = user
	flash('Successfully logged in')
	return redirect(url_for('home'))