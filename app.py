from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'secret'
app.permanent_session_lifetime = timedelta(days=5)  # setting up permanent session (5 days period)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'   # config, users is table name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):       # db model, represents db entity
    _id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

# @app.route('/<name>')
# def index(name):
#     last_name = name * 2
#     letters = list('abcdefgh')
#     return render_template('index.html', name=name, last_name=last_name, letters=letters)


# @app.route('/users/<user_id>')
# def user(user_id):
#     return f'User with id {user_id}'
#
#
# @app.route('/admin')
# def admin():
#     return redirect(url_for('user', user_id=10))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user' in session:                       # if user wants to login but their data is still stored in session
            flash('Already logged in.', 'info')
            return redirect(url_for('user'))        # redirect to user page instead of opening login form

        return render_template('login.html')        # if user data not in session, open login form
    else:
        session.permanent = True    # turning on permanent sessions
        username = request.form['username']         # get username from login form
        session['user'] = username                  # and store it in session

        found_user = User.query.filter_by(name=username).first()    # find user in db by given username
        if found_user:                              # if user exists in the db
            session['email'] = found_user.email     # store his email in session
        else:
            usr = User(name=username, email='')     # if it is a new user, create a new db model object with username
            db.session.add(usr)                     # and no email (yet), add user to db
            db.session.commit()                     # commit changes

        flash('Logged in successfully.', 'info')
        return redirect(url_for('user'))


@app.route('/logout')
def logout():
    session.pop('user', None)  # removing data from session
    flash('Successfully logged out.', 'info')
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/user', methods=['GET', 'POST'])
def user():
    email = None
    if 'user' in session:                   # if user data in session
        username = session['user']
        if request.method == 'POST':        # post email
            email = request.form['email']   # get email from the form
            session['email'] = email        # save it in session
            found_user = User.query.filter_by(name=username).first()    # find user in db by their username
            found_user.email = email        # [found_user is type User(db.Model) assign user's email
            db.session.commit()             # commit changes

            flash('Email saved.')
        else:
            if 'email' in session:          # GET: get email from session and pass it to the user page template
                email = session['email']

        return render_template('user.html', email=email)
    else:
        flash('You are not logged in.', 'info')
        return redirect(url_for('login'))


"""
HOW TO DELETE FROM DB

user_in_db = User.query.filter_by(id=1)
user_in_db.delete()
db.commit()
"""


@app.route('/view')  # for displaying all records stored in the database
def view():
    return render_template('view.html', db_records=User.query.all())


if __name__ == '__main__':
    db.create_all()     # initiate db
    app.run(debug=True)
