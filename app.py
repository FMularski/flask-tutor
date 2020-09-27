from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'secret'
app.permanent_session_lifetime = timedelta(days=5)  # setting up permanent session (5 days period)

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
        if 'user' in session:
            return redirect(url_for('user'))

        return render_template('login.html')
    else:
        session.permanent = True    # turning on permanent sessions
        username = request.form['username']
        session['user'] = username
        return redirect(url_for('user'))


@app.route('/logout')
def logout():
    session.pop('user', None)   # removing data from session
    return redirect(url_for('login'))


@app.route('/user')
def user():
    if 'user' in session:
        username = session['user']
        return f"<h1>{username}</h1>"
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
