from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


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
        return render_template('login.html')
    else:
        username = request.form['username']
        return redirect(url_for('user', usr=username))


@app.route('/<usr>')
def user(usr):
    return f'<h1>{usr}</h1>'


if __name__ == '__main__':
    app.run(debug=True)
