from flask import Blueprint, render_template


blp = Blueprint('auth', 'auth')

@blp.route('/login')
def login():
    return render_template('login.html')

@blp.route('/')
def splash():
    return render_template('splash_screen.html')





