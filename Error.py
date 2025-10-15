from colorama import init, Fore, Style
from reprStr import Print
import sys

init(autoreset=True)

# Custom Exceptions
class SemanticError(Exception): pass
class UnknownError(Exception): pass
class ParseError(Exception): pass

# Error code mapping
errors = {
    '0': UnknownError,
    '1': SyntaxError,
    '2': SemanticError,
    '3': ParseError,
}

def Raise(code_part=None, error_code=None, message=None, propagate=True):
    error_class = errors.get(str(error_code), UnknownError) if error_code is not None else UnknownError
    msg = message or "Unknown error"
    header = Style.BRIGHT + Fore.RED + f"{error_class.__name__}\n" + Style.RESET_ALL
    body = ""
    if code_part:
        code_lines = Print(code=code_part, gutter=False, print_=False, gutter_offset=0).splitlines()
        body = "\n".join([Style.BRIGHT + Fore.MAGENTA + f"  >>> {line}" + Style.RESET_ALL for line in code_lines]) + '\n'
    footer = Fore.GREEN + f"=> {msg}" + Style.RESET_ALL
    print(header + body + footer)
    
    if propagate:
        sys.exit(1)
