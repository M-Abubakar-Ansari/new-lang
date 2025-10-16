
lang_builtins = [
    'display',
    'num',
    'string',
    'is_positive'
]

prefix = 'py_py__'

# Constants

def py_py__display(*args, end = '\n'):
    print(*args, end=end)

def py_py__is_positive(n):
    return n > 0

class num:
    def __init__(self, value) -> None:
        self.value = value
    
    def toPy(self) -> str:
        return f"{self.value}"

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.__repr__()

class string:
    def __init__(self, value: str) -> None:
        self.value = value

    def toPy(self) -> str:
        return f'"{self.value}"'

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.__repr__()
