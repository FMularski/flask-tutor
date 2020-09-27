from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route('/<name>')
def index(name):
    last_name = name * 2
    letters = list('abcdefgh')
    return render_template('index.html', name=name, last_name=last_name, letters=letters)


# @app.route('/users/<user_id>')
# def user(user_id):
#     return f'User with id {user_id}'
#
#
# @app.route('/admin')
# def admin():
#     return redirect(url_for('user', user_id=10))


if __name__ == '__main__':
    app.run()
