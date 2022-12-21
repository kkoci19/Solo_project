from the_wall.models.user import User
from flask_bcrypt import Bcrypt
from the_wall import app
from flask import redirect, render_template, request, session, flash

from datetime import datetime, date

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

bcrypt = Bcrypt(app)

user = User()

app.secret_key = 'Yankees Suck'


class Users:
    def index(self):
        return render_template('index.html')

    def createUser(self):
        if len(request.form['first_name']) < 1:
            flash('*First name cannot be blank', 'first_name')
        if len(request.form['last_name']) < 1:
            flash('*Last name cannot be blank', 'last_name')
        if len(request.form['email']) < 1:
            flash('*Email cannot be blank', 'email')
        if not EMAIL_REGEX.match(request.form['email']):
            flash("*Invalid email", 'email')
        if len(request.form['password']) < 8:
            flash('*Password must be at least 8 characters.', 'password')
        if request.form['birthday'] == '':
            flash('*Confirm password!', 'c_password')
        if request.form['password'] != request.form['c_password']:
            flash('*Passwords do not match', 'c_password')
        if '_flashes' in session.keys():
            return redirect("/")
        else:
            result = user.checkUser()
            if result:
                flash("*Email used. Use alternative or log in to proceed.", 'email')
                return redirect('/')
            else:
                pw_hash = bcrypt.generate_password_hash(
                    request.form['password'])
                return user.newUser(pw_hash)

    def registration_success(self):
        flash("*User registered. Log-in to continue")
        return redirect('/')

    def log_in(self):
        if len(request.form['log_email']) < 1:
            flash('*Please enter email!', 'log_email')
        if len(request.form['log_password']) < 1:
            flash('*Please enter password.', 'log_password')
            return redirect('/')
        result = user.log_in()
        if result:
            print(result)
            if bcrypt.check_password_hash(result[0]['password'], request.form['log_password']):
                session['email'] = result[0]['email']
                session['first_name'] = result[0]['first_name']
                session['user_id'] = result[0]['id']
                return redirect('/dashboard')
            else:
                flash('Incorrect password', 'log_password')
                return redirect('/')
        flash('*User not registered. Please register first', 'log_email')
        return redirect('/')

    def dashboard(self):
        if 'email' not in session:
            return redirect('/hack')
        else:
            result = user.all_messages()
            comment = user.post_comment_update()
            return render_template('dashboard.html', messages=result, comments=comment)

    def post_message(self):
        if len(request.form['message']) < 1:
            flash('Enter some content', 'message')
            return redirect('/dashboard')
        else:
            return user.post_message()

    def message_success(self):
        flash('Message posted', 'message')
        return redirect('/dashboard')

    def logout(self):
        session.clear()
        return redirect('/')

    def post_comment(self, id):
        if len(request.form['comment']) < 1:
            flash('Please enter comment')
            return redirect('/dashboard')
        else:
            return user.post_comment(id)

    def comment_success(self):
        flash('Comment posted', 'comment')
        return redirect('/dashboard')
