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
    hookes = []
    for i in ast:
        if isi(i, EOL):
            lines.append(line.copy())
            line.clear()
        else:
            line.append(i)
    if line:
        lines.append(line.copy())
    return lines
