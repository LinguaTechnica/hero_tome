from flask import Flask, render_template, redirect, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/signup')
def signup_form():
    """Renders sign-up form"""
    app.logger.info('Rendering sign-up form ...')
    return render_template('signup.html')


@app.route('/api/signup', methods=['POST'])
def signup():
    """
    Handle signup form.
    Requires username, email, password and password confirmation.
    """
    app.logger.info('Creating new user ...')
    user_data = request.form
    app.logger.info(f'User data: {user_data}')

    return redirect('heroes/list.html')
