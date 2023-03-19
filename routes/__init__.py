"""Routes.__init.py
"""
import bottle
import lib

def session(authenticate : bool = True) -> lib.Session|None:
    """Access the session cookie.

    If the session cookie 
    """
    session = lib.Session()

    if not authenticate:
        return session
    
    if authenticate and 'id' not in session:
        request = bottle.request

        loginpath = request.app.config.get('app.loginpath', '/login')
        next = request.url or '/'
        bottle.redirect(f'{loginpath}?next={next}')
