import hashlib
import bottle
import lib
import lib.statements
import sqlite3 as sql


app =lib.app
userstatements = lib.statements.StatementRegister(app, 'users')


def hashpassword(password : str):
    """Hash password
    """
    if password:
        m = hashlib.sha512(password.encode())
        return m.hexdigest()


@app.route('/login')
@bottle.view('login')
def login():
    """
    """
    return dict(
        config=app.config
    )


@app.route('/login', method ='POST')
def loginapi(db : sql.Connection):
    """
    """
    def getparameters():
        """
        """
        forms = bottle.request.forms
        username = forms.get('username')
        password = forms.get('password')

        if username and password:
            return dict(
                username=username
                , passwordhash=hashpassword(password)
            )

    parameters = getparameters()
    if not parameters:
        bottle.abort(400, 'Malformed request: missing user name or password')
    
    recordset = userstatements.execute('login', db, parameters)
    match recordset.rowcount:
        case 0:
            bottle.abort(404, 'Not Found: ')

        case 1:
            user = recordset.rows[0]
            session = lib.Session()
            session['id'] = user['id']
            session['admin'] = user['useradmin']
 
            next = bottle.request.query.get('next') or '/'
            bottle.redirect(next)
    
        case _:
            bottle.abort(500, f'user.fetch returned {recordset.rowcount} rows')        