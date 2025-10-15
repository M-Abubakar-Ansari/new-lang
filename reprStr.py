from colorama import init, Fore, Back, Style
import math

init(autoreset=True)

class ColorDict(dict):
    def __getitem__(self, key):
        if key in self:
            return super().__getitem__(key)
        return lambda val: Style.BRIGHT + Fore.RED + str(val) + Style.RESET_ALL

Colors = ColorDict({
    'num': lambda val: Style.BRIGHT + Fore.GREEN + str(val) + Style.RESET_ALL,
    'str': lambda val: Style.DIM + Fore.RED + str(val) + Style.RESET_ALL,
    'opt': lambda val: str(val),
    'kwd': lambda val: Fore.MAGENTA + str(val) + Style.RESET_ALL,
    'idf': lambda val: Fore.CYAN + str(val) + Style.RESET_ALL,
    'fun': lambda val: Fore.YELLOW + str(val) + Style.RESET_ALL,
    'cls': lambda val: Fore.GREEN + str(val) + Style.RESET_ALL,
    'cot': lambda val: Fore.BLUE + str(val) + Style.RESET_ALL,
    'var': lambda val: Fore.CYAN + str(val) + Style.RESET_ALL,
})

def Indent(spaces, tabsize=4):
    tabs = math.ceil(spaces / tabsize)
    return tabs

def Print(code, gutter=True, print_ = True, gutter_offset = 1):
    """
    Pretty prints code with line numbers and indents
    """
    code = str(code)
    lines = code.splitlines()
    max_gutter = len(str(len(lines)))
    pretty = ''
    for i, line in enumerate(lines):
        raw_ind = len(line) - len(line.lstrip())
        ind_value = Indent(raw_ind)
        line_no = f"{str(i + 1).rjust(max_gutter)}|"
        pretty += f"{Fore.CYAN}{line_no if gutter else ''}{Style.RESET_ALL}{' '*gutter_offset}{' '*ind_value}{line.lstrip()}\n"
    if print_:
        print(pretty)
    return pretty
