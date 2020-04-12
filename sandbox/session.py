from flask import Flask, session, redirect, url_for, request
from markupsafe import escape

app = Flask(__name__)


app.secret_key = b'\xdf\x1a\x08T>,\x91/\x04\xf9\x94nD\xf04h'

@app.route('/')
def index():
    ##logging example
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    if 'username' in session:
        return f'Logged in as {escape(session["username"])}'
    return 'You are not logged in'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the username form the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))