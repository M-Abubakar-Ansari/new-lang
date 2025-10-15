from astSource import *
from string import punctuation
from Error import Raise

variables = []
functions = []
classes = []
isi = isinstance

def isIdentifier(name: str): 
    return bool(name) and not name[0].isdigit() and not any(c in punctuation.replace('_','') for c in name)

def astToLines(ast):
    lines = []
    line = []
    for i in ast:
        if isi(i, EOL):
            lines.append(line.copy())
            line.clear()
        else:
            line.append(i)
    if line:
        lines.append(line.copy())
    return lines

# ...existing code...
def astToPy(ast):
    pyLines = []
    for line in ast:
        py_line = []
        indent = ''
        for a in line:
            if isi(a, INDENT):
                indent = a.toPy()
            elif isi(a, Keyword):
                if a.value == 'is':
                    py_line.append('=')
                elif a.value == 'gives':
                    py_line.append('return')
                elif a.value == 'fun':
                    continue
                else:
                    py_line.append(a.toPy() or a.value)
            elif isi(a, Operator):
                py_line.append(a.toPy() or a.value)
            elif isi(a, Conditional):
                # Always use the correct Python keyword for conditionals
                py_keyword = a.py_type  # should be 'if', 'elif', or 'else'
                cond_str = ''
                if isinstance(a.cond, list):
                    cond_str = ' '.join(
                        x.value if isi(x, Identifier) else str(x.value) if isi(x, num) else str(x)
                        for x in a.cond
                    )
                else:
                    cond_str = str(a.cond)
                if py_keyword == 'else':
                    py_line.append(f"{py_keyword}:")
                else:
                    py_line.append(f"{py_keyword} {cond_str}:")
            elif isi(a, FunctionDef):
                params = ', '.join([p.value for p in a.params if isi(p, Identifier)])
                py_line.append(f'def {a.name}({params}):')
            elif isi(a, FunctionCall):
                args = ', '.join([arg.value if isi(arg, Identifier) else str(arg.value) if isi(arg, num) else str(arg) for arg in a.args])
                py_line.append(f'{a.name}({args})')
            elif isi(a, Identifier):
                py_line.append(a.value)
            elif isi(a, num):
                py_line.append(str(a.value))
            elif isi(a, string):
                py_line.append(f'"{a.value}"')
            else:
                val = getattr(a, 'value', None)
                if val is not None:
                    py_line.append(str(val))
        if py_line:
            pyLines.append([indent + ' '.join(py_line)])
        else:
            pyLines.append([indent])
    return pyLines
# ...existing code...

def lineToPy(lines):
    code = ''
    for i in lines:
        c = ''.join(i)
        code += c.rstrip() + '\n'
    return code