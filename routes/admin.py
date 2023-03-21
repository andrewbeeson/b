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
    """Present an administration page for user data.

    Allows:
     1. User selection by system identifier (id) and by name, and
     2. User listing by active/inactive or admin/user flags.

    The identification order is:
         1. any individual by id
         2. any individual by name
         3, all individuals by partial name, active and admin
         4, all individuals by partial name and active
         5, all individuals by partial name and admin
         6. all individuals by partial name 
         7. all individuals by active and admin
         8. all individuals by active
         9. all individuals by admin
        10. all individuals
    """
    checkadmin()

    query = bottle.request.query

    active : bool = None if not query.get('active') else bool(int(query['active']))
    admin : bool = None if not query.get('admin') else bool(int(query['admin']))
    id : int = None if not query.get('id') else int(query['id'])
    name : str = str(query.get('name'))

    parameters = dict(active=active, useradmin=admin, id=id, name=name)

    activeinactive = 'active' if active else 'inactive'
    adminsplayers = 'administrators' if admin else 'players'
    
    if id:
        selection = f'Individual with id, {id}'
        statement = 'fetch by id'

    elif name and '%' not in name and '_' not in name:
        selection = f'Individual with name, {name}'
        statement = 'fetch by name'
    
    elif name and active is not None and admin is not None:
        selection = f'All {activeinactive} {adminsplayers} with name matching {name}'
        statement = 'list by partial name, active and admin'
    
    elif name and active is not None:
        selection = f'All {activeinactive} individuals with name matching {name}'
        statement = 'list by partial name and active'
    
    elif name and admin is not None:
        selection = f'All {adminsplayers} with name matching {name}'
        statement = 'list by partial name and admin'
    
    elif name:
        selection = f'All individual with name matching {name}'
        statement = 'list by partial name'
    
    elif active is not None and admin is not None:
        selection = f'All {activeinactive} {adminsplayers}'
        statement = 'list by active and admin'
    
    elif active is not None:
        selection = f'All {activeinactive} individuals'
        statement = 'list by active'
    
    elif admin is not None:
        selection = f'All {adminsplayers}'
        statement = 'list by admin'
    
    else:
        selection = f'All individuals'
        statement = 'list all'

    if statement:
        resultset = userstatements.execute(statement, db, parameters)

    else:
        resultset = lib.statements.ResultSet()    
    
    return dict(
        config=bottle.request.app.config
        , parameters=parameters
        , resultset=resultset.todict()
        , selection = selection
        , url=bottle.request.url
    )