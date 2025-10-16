# Transpiler.py
from astSource import *
from Builtins import lang_builtins, prefix
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

def astToPy(ast):
    pyLines = []
    
    def serialize_token(tok, in_expr=False):
        """Serialize token without color codes"""
        if isi(tok, Identifier):
            return prefix + tok.value if not tok.value.startswith(prefix) else tok.value
        if isi(tok, num):
            return str(tok.value)  # Direct number output
        if isi(tok, string):
            return f'"{tok.value}"'
        if isi(tok, Operator):
            return operators.get(tok.value, tok.value)
        if isi(tok, FunctionCall):
            args = []
            curr_expr = []
            
            for arg in tok.args:
                if isi(arg, SEP):
                    if curr_expr:
                        args.append(' '.join(serialize_token(t, True) for t in curr_expr))
                        curr_expr = []
                else:
                    curr_expr.append(arg)
            
            if curr_expr:
                args.append(' '.join(serialize_token(t, True) for t in curr_expr))
            
            name = prefix + tok.name if not tok.name.startswith(prefix) else tok.name
            return f"{name}({', '.join(args)})"
        
        v = getattr(tok, 'value', None)
        return str(v) if v is not None else str(tok)

    for line in ast:
        py_line = []
        indent = ''
        for a in line:
            if isi(a, INDENT):
                indent = a.toPy()
            elif isi(a, FunctionDef):
                params = ', '.join(serialize_token(p) for p in a.params)
                name = prefix + a.name if not a.name.startswith(prefix) else a.name
                py_line.append(f"def {name}({params}):")
            elif isi(a, FunctionCall):
                # Handle nested function calls in arguments
                args = []
                curr_expr = []
                
                for arg in a.args:
                    if isi(arg, SEP):
                        if curr_expr:
                            args.append(' '.join(serialize_token(t, True) for t in curr_expr))
                            curr_expr = []
                    else:
                        curr_expr.append(arg)
                
                if curr_expr:
                    args.append(' '.join(serialize_token(t, True) for t in curr_expr))
                
                name = prefix + a.name if not a.name.startswith(prefix) else a.name
                py_line.append(f"{name}({', '.join(args)})")
            elif isi(a, Keyword):
                if a.value == 'is':
                    py_line.append('=')
                elif a.value == 'gives':
                    py_line.append('return')
                elif a.value == 'fun':
                    continue
                else:
                    py_line.append(serialize_token(a))
            elif isi(a, Conditional):
                cond = []
                if a.cond:  # Check if condition exists
                    for c in a.cond:
                        if isi(c, Identifier):
                            cond.append(prefix + c.value if not c.value.startswith(prefix) else c.value)
                        elif isi(c, num):
                            cond.append(str(c.value))
                        elif isi(c, Operator):
                            cond.append(operators.get(c.value, c.value))
                        elif isi(c, FunctionCall):
                            cond.append(serialize_token(c, True))
                        else:
                            cond.append(serialize_token(c))
                    py_line.append(f"if {' '.join(cond)}:")
                else:
                    py_line.append("if True:")
            else:
                py_line.append(serialize_token(a))
        
        if py_line:
            pyLines.append([indent + ' '.join(py_line)])
        else:
            pyLines.append([indent])
            
    return pyLines
def lineToPy(lines):
    code = ''
    for i in lines:
        c = ''.join(i)
        code += c.rstrip() + '\n'
    return code

def run(lines):
    exec(lines)