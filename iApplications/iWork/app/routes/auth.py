from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import login_required, login_user, logout_user
from passlib.hash import pbkdf2_sha256

from iWork.app.models import User

blp = Blueprint("auth", "auth")

@blp.route('/login',methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()       
        if user:
            db_username = user.username
            db_pass = user.password
            hash_check = pbkdf2_sha256.verify(password,db_pass)        
            if db_username == username and hash_check:
                login_user(user)
                return redirect(url_for('routes.profile'))
        else:
            flash('Please Check your login credentials and try again !! ')
            return redirect(url_for('auth.login'))
        
    return render_template('login.html')


@blp.route('/register',methods=["POST","GET"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        name = request.form.get('name')
        password = pbkdf2_sha256.hash(request.form.get('password'))

        user = User.get_user_by_username(username)
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        user = User(name,username,password)
        user.save_to_db()
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@blp.route('/logout')
@login_required
def logout():    
    logout_user()
    session['logged_out']=True
    return redirect(url_for('.login'))


   
@blp.route('/change_password/<id>',methods=['GET','POST'])
@login_required
def change_password(id):

    if request.method == "POST":
            
        current_pwd = request.form.get('curr_pwd')
        new_pwd = pbkdf2_sha256.hash(request.form.get('new_pwd'))

        user = User.query.filter_by(id=id).first()       
        if user:
        
            db_pass = user.password
            hash_check = pbkdf2_sha256.verify(current_pwd,db_pass)        
            if hash_check:
                data = {"password":new_pwd}
                User.update_db(data,id)   

                return redirect(url_for('route.profile'))
            
            else:
                flash('Please Check Your Old Password and Try Again !! ')
                return redirect(url_for('auth.change_password',id=id))
    
    if request.method == "GET":
        user=User.get_user_by_id(id)
        
        return render_template('change_password.html',user=user)
   