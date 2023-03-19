"""lib


"""
import hashlib
import os
import sys
import time
import typing

import bottle

import lib.dbplugin


def config(app : bottle.Bottle) -> None:
    """Load configurations to the app
    """
    def paths() -> str:
        try:
            i = 0
            while True:
                i = sys.argv.index('-c', i) + 1
                yield sys.argv[i]
        
        except ValueError:
            if i == 0 and os.path.exists('test.cfg'):
                yield 'test.cfg'
    
    print('Configurations:')
    i = 0
    for path in paths():
        if os.path.exists(path):
            app.config.load_config(path)
            i += 1
            print(f'\t{path}')
    
    if i == 0:
        print('\tNone')


def hashsecret(secret : str) -> str:
    """Hash passwords and other secrets
    """
    secretbytes =secret.encode(encoding='utf=8')
    m = hashlib.SHA512(secretbytes)
    return m.hexdigest()


def routes(app):
    """Add the routes defined in the given modules.
    The route modules are listed in the 'modules' entry in the 'routes' 
    configuration section. Go figure.

    TODO: The exec command is used to import each module. This should be replaced 
    via the importlib module.
    """
    modules = app.config.get('routes.modules', '').split()
    if modules:
        print('Importing route modules:')
        for module in modules:
            try:
                print(f'\t{module}')
                exec(f'import {module}', globals(), locals())

            except ModuleNotFoundError:
                print(f'\t\t{module} not found')

    else:
        print('Configuration entry, routes.modules, is missing: no routes configured')

    if app.routes:
        print('Active routes:')
        for route in app.routes:
            print(f'\t{route.rule}({route.method}): {route.callback.__name__}')

    else:
        print('No active routes')


def run() -> None:
    """Run the application
    """
    def configure():
        return dict(
            debug = app.config.get('app.debug')
            , host = app.config.get('app.host')
            , port = app.config.get('app.port')
            , reload = app.config.get('app.reload')
            , server = app.config.get('app.server')
        )
    
    def clean():
        return dict((k, v) for k, v in kwargs.items() if v != None)

    def log():
        if len(kwargs) == 0:
            print('Running with defaults.')
    
        else:
            print('Run parameters:')
            for parameter, value in kwargs.items():
                print(f'\t{parameter}: {value}')

    kwargs = configure()
    kwargs = clean()
    log()
    app.run(**kwargs)


class Session(object):
    """
    """
    __slots__ = ('_data', 'maxage', 'name')

    secret = 'where, oh, where has my data gone?'

    def __init__(self):
        """
        """
        app = bottle.request.app

        self.maxage : int = app.config.get('app.maxage')
        self.name : str = app.config.get('app.name').replace(' ', '_')

        print('Session:', f'getting cookie at {time.time()}')
        data : dict = bottle.request.get_cookie(self.name, secret=self.secret)
        print('Session:', f'got cookie at {time.time()}')
        self._data : dict = data or dict()

    def __contains__(self, key):
        """
        """
        return self._data.__contains__(key)

    def __delitem__(self, key):
        """
        """
        return self._data.__delitem__(key)

    def __getitem__(self, key):
        """
        """
        return self._data.__getitem__(key)

    def __hasitem__(self, key):
        """
        """
        return self._data.__hasitem__(key)

    def __setitem__(self, key, value):
        """
        """
        result = self._data.__setitem__(key, value)
        print('Session:', f'setting cookie at {time.time()}')
        bottle.response.set_cookie(
            self.name, self._data, max_age=self.maxage, secret=self.secret
        )
        print('Session:', f'set cookie at {time.time()}')
        
        return result

    def get(self, key : typing.Any, default : typing.Any = None) -> typing.Any:
        """
        """
        return self._data.get(key, default)


def sqlite3(app):
    """Install the SQLite plug-in.
    """
    dburl = app.config.get('sqlite.dburl')
    keyword = app.config.get('sqlite.keyword', 'db')
    if dburl:
        print(f'Database (sqlite) at {dburl}')
        plugin = lib.dbplugin.Plugin(dburl=dburl, keyword=keyword)
        app.install(plugin)

    else:
        print(
            'Configuration entry, sqlite3.dburl, is missing: '
            + 'SQLite3 not configured'
        )


app = bottle.Bottle()
config(app)
routes(app)
sqlite3(app)