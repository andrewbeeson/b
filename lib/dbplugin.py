"""
"""

import sqlite3 as sql
import inspect
import bottle


class DbAPI2Plugin(object):
    """
    """
    __slots__ = ('dburl', 'keyword')

    name = 'dbapi2'
    api = 2

    def __init__(self, dburl, keyword='db'):
        self.dburl = dburl
        self.keyword = keyword

    def setup(self, app):
        """
        """
        cls = self.__class__
        clsname = cls.__name__
        for other in app.plugins:
            if not isinstance(other, cls):
                continue

            if other.keyword == self.keyword:
                msg = f"Multiple {clsname} plugins using keyword {self.keyword}"
                raise bottle.PluginError(msg)

            if other.name == self.name:
                self.name = f'{self.name}_{self.keyword}'

    def apply(self, callback, route):
        """
        """
        config = route.config
        _callback = route.callback

        dburl = config.get('sqlite.dburl', self.dburl)
        keyword = config.get('sqlite.keyword', self.keyword)
        
        signature = inspect.signature(_callback)
        if keyword not in signature.parameters:
            return _callback

        def wrapper(*args, **kwargs):
            db : sql.Connection = sql.connect(dburl)
            db.row_factory = sql.Row
            kwargs[keyword] : sql.Connection = db

            try:
                rv = callback(*args, **kwargs)
                if db.in_transaction:
                    db.commit()
                
                return rv
            
            except sql.IntegrityError as e:
                if db.in_transaction:
                    db.rollback()
                
                raise bottle.HTTPError(500, "Database Error", e)
            
            except bottle.HTTPResponse as e:
                if db.in_transaction:
                    db.commit()
                
                raise
            
            finally:
                db.close()
            
        return wrapper

Plugin = DbAPI2Plugin
