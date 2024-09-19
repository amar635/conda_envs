
from flask import Blueprint, redirect, render_template, url_for
from flask_login import logout_user

blp = Blueprint("auth", "auth")

# Login route
@blp.route('/login', methods=['GET', 'POST'])
def login():
    # Handle login logic, generate JWT token, and redirect to the requested app
    return render_template('login.html')

@blp.route('/logout')
def logout():
    logout_user()
    # Invalidate the JWT token as needed
    return redirect(url_for('login'))