from markupsafe import escape
from flask import Flask, request, render_template, url_for
import flask

app = Flask(__name__)


@app.route('/api/me')
def me_api():
    game = {
        'subject': 'Animals',
        'words':  ['dog', 'cat', 'emu', 'rabbit']
    }
    return game


@app.route('/api/animals')
def animal_api():
    animals = ['dog', 'cat', 'emu', 'rabbit']
    return flask.jsonify(animals)

@app.route('/')
def index():
    # Reading cookies
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a 
    # `KeyError` if the cookie is missing.

    resp = flask.make_response(render_template('hello.html'))
    resp.set_cookie('username', 'the username')
    return resp


@app.route('/redirect')
def _redirect():
    return flask.redirect(url_for('redirect_login'))


@app.route('/redirect_login')
def redirect_login():
    flask.abort(401)


@app.errorhandler(404)
def page_not_found(error):
    # the 2nd value tells flask which status code to return
    return render_template('page_not_found.html'), 404


## Modifying response object
@app.errorhandler(404)
def not_found(error):
    resp = flask.make_response(render_template('hello.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        return 'do the login'
    else:
        error = 'Invalid username/password'
        # the code below is executed if the request method
        # was GET or the credentials were invalid
        return render_template('hello.html', error=error)


@app.route('/user/<username>')
def profile(username):
    # show the user profile for that user
    return f'User {escape(username)}'


with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
    print(url_for('static', filename='style.css'))

# for unit testing to make request context available to the application
with app.test_request_context('/hello', method='POST'):
    # now you can do something with the request util the
    # end of the with bloc, such as basic assertions:
    print(f'request.path=={request.path}')
    print(f'request.method=={request.method}')
    assert request.path == '/hello'
    assert request.method == 'POST'


@app.route('/projects/')
def projects():
    return f'The projectpage'


@app.route('/about')
def about():
    return f'The about page'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return f'Post {post_id}'


@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return f'Subpath {escape(subpath)}'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
