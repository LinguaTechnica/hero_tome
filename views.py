from flask import Flask, render_template, redirect, request, session

from models import User

app = Flask(__name__)


# Visitor Routes
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login_form():
    return render_template('login.html')


@app.route('/signup')
def signup_form():
    """Renders sign-up form"""
    app.logger.info('Rendering sign-up form ...')
    return render_template('signup.html')


# Auth Routes
@app.route('/api/auth', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form.get('username')).first()

    # Check password
    if user.login(request.form.get('password')):
        app.logger.info('Login successful ...')
        session['user_id'] = user.id
    else:
        app.logger.info('Login failed!')
        return render_template('login.html')

    return render_template('users/detail.html', user=user)


@app.route('/logout')
def logout():
    del session['user_id']

    return redirect('/')


@app.route('/api/signup', methods=['POST'])
def signup():
    """
    Handle signup form.
    Requires username, email, password and password confirmation.
    """
    app.logger.info('Creating new user ...')
    # Create a copy so I can edit the dictionary later
    user_data = dict(request.form)

    if user_data.get('password') == user_data.get('passwordConf'):
        # User data must contain only valid fields. Remove invalid
        del user_data['passwordConf']

        # TODO: Refactor - create utility function that creates users
        user = User(**user_data)
        user.create_password(user_data.get('password'))
        user.save()
        app.logger.info(f'User {user.id} created. Logging in...')
        session['user_id'] = user.id

        return redirect(f'/users/{user.id}')


# User Routes
@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    app.logger.info(f'Current user: {user}')

    return render_template('users/detail.html', user=user)


# Hero Routes
