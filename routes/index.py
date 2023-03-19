"""
"""

import bottle
import lib
import lib.statements
import routes
import sqlite3 as sql


app = lib.app


@app.route('/static/<filename>')
def server_static(filename):
    """Return static file to the client
    """
    staticpath = app.config.get('static.path')

    return bottle.static_file(filename, root=staticpath)


@app.route('/')
@bottle.view('index')
def index(db):
    """
    """
    request = bottle.request
    userstatements = lib.statements.StatementRegister(app, 'users')
    session = lib.Session()
    if 'id' not in session:
        loginpath = lib.app.config.get('app.loginpath', '/login')
        next = request.url or '/'
        bottle.redirect(f'{loginpath}?next={next}')

    parameters = dict(id=session['id'])
    resultset = userstatements.execute('fetch by id', db, parameters)

    return dict(resultset=resultset, config=app.config)