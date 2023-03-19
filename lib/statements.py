
"""
"""
import bottle
import io
import os
import sqlite3 as sql
import typing


class Record(object):
    """
    """
    __slots__ = ('active', 'id', 'revision')

    @classmethod
    def _slots(cls) -> set:
        """
        """
        attributenames = set()

        for c in cls.mro():
            slots = getattr(c, '__slots__', tuple())
            attributenames.update(slots)
        
        return attributenames

    def __init__(self, **attrs):
        """
        """
        for slot in self._slots():
            setattr(self, slot, attrs.get(slot))

    @classmethod
    def fromdict(cls, attrs) -> typing.Any:
        """Returns a record of this type based on the given attribte key-value pairs.
        """
        return cls(**attrs)

    def todict(self) -> dict:
        """Returns a dict representing the attributes of this record.
        """
        return dict(
            (slot, getattr(self, slot, None))
            for slot in self._slots()
        )


class ResultSet(object):
    """Results returned by a cursor

        lastrowid:  the row id allocated by the most recent statement (0 if the 
                    most recent statement didn't insert a row)
        lastcount:  the count of rows effected by the most recent statement (-1
                    if the most recent statement was not intended to insert, 
                    update or delete any rows)
        rowcount:   the number of rows returned by the last statement
        rows:       a list of Record objects (or dicts if rowclass is None) 
                    where each object or dict represents a row
    """
    __slots__ = ('lastcount', 'lastrowid', 'rowcount', 'rows')

    def __init__(self, cursor : sql.Cursor=None, rowclass : typing.Type = None):
        """
        """
        if rowclass is None: 
            rowclass = dict

        if cursor:
            self.lastrowid = cursor.lastrowid
            self.lastcount = cursor.rowcount
            self.rows = list(
                rowclass(**row) if isinstance(row, dict) else row
                for row in cursor.fetchall()
            )
            self.rowcount = len(self.rows)

        else:
            self.lastrowid = -1
            self.lastcount = 0
            self.rows = list()
            self.rowcount = 0

    def todict(self) -> dict:
        """
        """
        return dict(
            lastcount=self.lastcount
            , lastrowid=self.lastrowid
            , rowcount=self.rowcount
            , rows=[dict(row) for row in self.rows]
        )


class Statement(object):
    """
    """
    __slots__ = ('name', 'parameternames', 'script', 'statement')

    @classmethod
    def parsefile(cls, path : str) -> dict[str, typing.Any] :
        """
        """
        with open(path, 'rt') as stream:
            statements = cls.parsestream(stream)
            return statements
        
    @classmethod
    def parsestream(cls, stream : io.TextIOWrapper) -> dict[str, typing.Any] :
        """
        """

        statements = dict()
        current = cls()
        for line in stream:
            new = current.parseline(line)
            if new:
                statements[current.name] = current
                current = new

        if current.isvalid:
            statements[current.name] = current
        
        return statements

    def __init__(
            self
            , name : str = None
            , parameternames : list[str] = list()
            , script: bool = False
            , statement : str = ''
        ):
        """
        """
        self.name = name
        self.parameternames = parameternames
        self.script = script
        self.statement = statement

    def __str__(self):
        """
        """
        return f'-- name: {self.name}-- parameters: {self.parameternames}{self.statement}'

    def execute(
        self
        , db : sql.Connection
        , parameters : dict[str, typing.Any] = dict()
        , rowclass : Record = None
    ) -> ResultSet :
        """Executes this statement.
        
        If self.script is True, the db.executescript is used
        """
        parametervalues = tuple(
            parameters.get(parametername) 
            for parametername in self.parameternames
        )
        
        cursor = None
        try:
            execute = db.executescript if self.script else db.execute
            cursor = execute(self.statement, parametervalues)
            
            resultset = ResultSet(cursor, rowclass or dict)
            return resultset
        
        finally:
            if cursor:
                cursor.close()

    @property
    def isvalid(self) -> bool:
        """
        """
        return (
            self.name 
            and self.statement 
            and isinstance(self.parameternames, list) 
            and isinstance(self.script, bool)
        )

    def parseline(self, line : str) -> typing.Any :
        """
        """
        if line.startswith('-- name:'):
            if self.isvalid:
                return self.__class__(name=line[8:].strip())
            
            if self.name:
                raise ValueError(f'Invalid:\n{self}')
            
            self.name = line[8:].strip()
        
        elif line.startswith('-- parameters:'):
            self.parameternames = line[14:].split()
        
        elif line.startswith('-- script:'):
            self.script = line[10:].strip() in '1tTyY'
        
        else:
            self.statement += line

        return None


class StatementRegister(object):
    """Register statements for a particular data domain.
    """
    __slots__ = ('domain', 'statements')


    def __init__(self, app : bottle.Bottle, domain : str, configsection : str = 'sql') -> None:
        """
        """
        self.domain = domain
        self.statements : dict[str, Statement] = dict()

        configpath = f'{configsection}.{domain}'
        statementpath = app.config.get(configpath)
        if not statementpath:
            raise ValueError(f'No configuration {configpath}')
        
        if not os.path.exists(statementpath):
            raise ValueError(f'No file {statementpath}')
        
        self.statements = Statement.parsefile(statementpath)

        names = '\n\t'.join(key for key in self.statements.keys())
        if not names:
            names = 'None'

        print(f'{domain} statements loaded:\n\t{names}')

    def execute(
        self
        , name : str
        , db : sql.Connection
        , parameters : dict[str, typing.Any] = dict()
        , rowclass : Record = None
    ) -> ResultSet:
        """
        """
        statement = self.statements[name]
        return statement.execute(db, parameters, rowclass)