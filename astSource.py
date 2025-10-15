from functools import wraps
from reprStr import Colors

operators = {
    '===': 'type', # Type
    '!==': 'not-type', # Type
    '->': 'in', # Membership
    ':>': 'not in', # Member ship
    '&&': '&', # Bitwise
    '||': '|', # Bitwise
    '~~': '~', # Bitwise
    '><': '^', # Bitwise
    '&': 'and', # Boolean
    '|': 'or', # Boolean
    '!': 'not', # Boolean
    '=': '==', # Relational
    '~': '!=', # Relational
    '>=' : '>=', # Relational
    '<=' : '<=', # Relational
    '>': '>', # Relational
    '<': '<', # Relational
    '//': '//', # Arithemtic
    '^': '**', # Arithemtic
    '+': '+', # Arithemtic
    '-': '-', # Arithemtic
    '*': '*', # Arithemtic
    '/': '/', # Arithemtic
    '%': '%', # Arithemtic,
}

keywords = {
    'its': 'self',
    'it' : 'self',
    'is' : '=',
    'fun': 'def',
    'new': 'class',
    'takes': '',
    'gives': 'return'
}

class num:
    def __init__(self, value) -> None:
        self.value = value
    
    def toPy(self) -> str:
        return f"{self.value}"
    
    def __repr__(self) -> str:
        return Colors['num'](self.value)

class string:
    def __init__(self, value: str) -> None:
        self.value = value

    def toPy(self) -> str:
        return f'"{self.value}"'

    def __repr__(self) -> str:
        return Colors['str'](f'"{self.value}"')

class INDENT:
    def __init__(self, value = 0) -> None:
        self.value = '    ' * int(value)
    
    def toPy(self):
        return self.value
    
    def __repr__(self) -> str:
        return f"INDENT({len(self.value) // 4})"

class EOL:
    def __init__(self) -> None:
        self.value = '\n'
    
    def toPy(self):
        return self.value
    
    def __repr__(self) -> str:
        return ";"

class Operator:
    def __init__(self, value) -> None:
        self.value = value

    def toPy(self) -> str|None:
        return operators.get(self.value.strip())

    def __repr__(self) -> str:
        return Colors['opt'](self.value)

class Keyword:
    def __init__(self, value) -> None:
        self.value = value

    def toPy(self) -> str|None:
        return keywords.get(self.value.strip())

    def __repr__(self) -> str:
        return Colors['kwd'](self.value)

class Identifier:
    def __init__(self, value) -> None:
        self.value = value
    
    def toPy(self):
        return f"{self.value}"

    def __repr__(self) -> str:
        return Colors['idf'](self.value)

class FunctionDef:
    def __init__(self, name, params=None):
        self.name = name
        if not params:  params = []
        self.params = params

    def toPy(self) -> str|None:
        return f"def {self.name}({self.params}):"

    def __repr__(self) -> str:
        return Colors['fun'](f"{self.name}({self.params})")

class FunctionCall:
    def __init__(self, name, args=None):
        self.name = name
        self.args = args or []
    
    def toPy(self) -> str|None:
        return f"{self.name}({self.args})"

    def __repr__(self) -> str:
        return Colors['fun'](f"{self.name}({self.args})")

class Conditional:
    def __init__(self, cond=None, pyType='if'):
        self.cond = cond if pyType != 'else' else ''
        self.py_type = pyType
    
    def toPy(self):
        return f"{self.py_type} {self.cond}:"
    
    def __repr__(self):
        return f"{Colors['kwd'](self.py_type)} {self.cond}"
