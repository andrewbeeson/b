"""
"""

import bottle
import sqlite3

import lib
import lib.statements


app =lib.app
userstatements = lib.statements.StatementRegister(app, 'users')


def checkadmin(abort : bool = True) -> bool:
    """
    """
    session : dict = lib.Session()
    admin = bool(session.get('admin', False))
    if abort and not admin:
        bottle.abort(403, 'Not authorised')

    return admin


@app.route('/admin/user', method='DELETE')
def usermaintenance(db):
    """
    """
    checkadmin()

    query = bottle.request.query

    id = query.get('id')
    revision = query.get('revision')
    if id is None or revision is None:
        bottle.abort(400, 'Bad Request')

    parameters = dict(id=id, revision=revision)
    recordset = userstatements.execute('deactivate user', db, parameters)
    return dict(recordset=recordset)


@app.route('/admin/user', method='GET')
@bottle.view('admin')
def usermaintenance(db):
    """
    """
    print('admin/user', 'Checking...')
    checkadmin()

    query = bottle.request.query

    active : int = int(query['active']) if 'active' in query else None
    admin : int = int(query['admin']) if 'admin' in query else None
    id : int = int(query['id']) if 'id' in query else None
    name : int = int(query['name']) if 'name' in query else None
    
    msg = f'active: {active}, admin: {admin}, id: {id}, name: {name}'
    print('admin/user', msg)

    if id:
        print('admin/user', f'accessing id={id}')
        statement = 'fetch by id'
        parameters = dict(id=id)

    elif name:
        print('admin/user', f'accessing name={name}')
        statement = 'fetch by name'
        if '%' in name or '?' in name:
            statement = 'list active by partial name'
    
        parameters = dict(name=name)
    
    elif active is not None and admin is not None:
        print('admin/user', f'accessing active={active}, admin={admin}')
        statement = 'list by active and admin'
        parameters = dict(active=active, admin=admin)
    
    elif active is not None:
        print('admin/user', f'accessing active={active}')
        statement = 'list by active'
        parameters = dict(active=active)
    
    else:
        print('admin/user', 'accessing none')
        statement = None
        parameters = dict()

    if statement:
        resultset = userstatements.execute(statement, db, parameters)

    else:
        resultset = lib.statements.ResultSet()    
    
    return dict(
        resultset=resultset.todict()
        , config=bottle.request.app.config
        , url=bottle.request.url
    )