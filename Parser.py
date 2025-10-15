# PARSER
import string as st
from astSource import *
import math
from Error import Raise

def Indent(spaces, tabsize=4):
    tabs = math.ceil(spaces / tabsize)
    return tabs

letters = st.ascii_letters
digits = st.digits
functions = []

def _filter_strings_and_identifiers(expr):
    in_string = False
    word = ''
    parts = []
    for i in expr:
        if in_string:
            word += i
            if i == '"':
                in_string = False
                parts.append(word)
                word = ''
        else:
            if i == '"':
                if word:
                    parts.append(word)
                    word = ''
                in_string = True
                word += i
            elif i.isspace():
                if word:
                    parts.append(word)
                    word = ''
            else:
                word += i
    if word:
        parts.append(word)
    return parts

def exprToAst(expr: str):
    tokens = _filter_strings_and_identifiers(expr)
    final_tokens = []
    for t in tokens:
        if t.startswith('"') and t.endswith('"'):
            final_tokens.append(t)
        elif t.replace('.', '', 1).isalnum() or t.replace('_','').isalnum():
            final_tokens.append(t)
        else:
            i = 0
            while i < len(t):
                matched = False
                for op in sorted(list(operators.keys()), key=lambda x: -len(x)):
                    if t[i:i+len(op)] == op:
                        final_tokens.append(op)
                        i += len(op)
                        matched = True
                        break
                if not matched:
                    final_tokens.append(t[i])
                    i += 1
    ast = []
    hooks = []
    thing_to_append = None
    for t in final_tokens:
        if t.startswith('"') and t.endswith('"'):
            thing_to_append = string(t[1:-1])
        elif t.replace('.', '', 1).isdigit():
            thing_to_append = (num(t))
        elif t in operators:
            thing_to_append = (Operator(t))
        elif t in keywords:
            thing_to_append = (Keyword(t))
        elif t in [i.get('obj').name for i in functions]:
            thing_to_append = (FunctionCall(t))
            hooks.append('fun-call')
        else:
            thing_to_append = Identifier(t)
        if thing_to_append:
            if hooks:
                if hooks[-1] == 'fun-call' and (not ast or not isinstance(ast[-1], FunctionCall)):
                    ast.append(thing_to_append)
                elif isinstance(ast[-1], FunctionCall):
                    ast[-1].args.append(thing_to_append)
            else:
                ast.append(thing_to_append)
    return ast

def variableToAst(expr):
    expr = str(expr).split('is', 1)
    name, value = expr[0], expr[1]
    name = name.strip()
    return [Identifier(name), Keyword('is'), *(exprToAst(value))]

def functionToAst(expr):
    expr = str(expr).split(' ')
    name = expr[1].removesuffix(':')
    return [FunctionDef(name)]

def sourceToAst(source):
    source = str(source).splitlines()
    hooks = []
    ast = []
    for l in source:
        l = l.rstrip()
        if not l: continue
        indent = Indent(l.rstrip().__len__() - l.strip().__len__())
        parts = _filter_strings_and_identifiers(l)
        length = len(parts)
        l = l.strip()
        ast_parts = None
        if length > 2 and parts[1] == 'is':
            ast_parts = variableToAst(l)
        elif parts[0] in ['if', 'elif', 'else'] and parts[-1][-1] == '?':
            ast_parts = [Conditional(exprToAst([(str(j).removesuffix('?') if i == len(parts[1:])-1 else j ) for i,j in enumerate(parts[1:])]), parts[0].lower())]
        elif parts[0] == 'fun' and str(parts[-1]).endswith(':'):
            ast_parts = functionToAst(l)
            indent_node = INDENT(indent)
            line_ast = [indent_node] + ast_parts + [EOL()]
            ast.extend(line_ast)
            functions.append({'obj': ast_parts[0], 'ind': len(ast) - len(line_ast)})
            hooks.append('pass')
        elif parts[0] in ['takes', 'gives']:
            isTake = parts[0] == 'takes'
            if isTake:
                ast_parts = exprToAst(' '.join(parts[1:]))
            else:
                ast_parts = exprToAst(l.replace('gives ', '', 1))
            if functions:
                fun_indent = ast[functions[-1].get('ind')-1].value
                if not fun_indent < Indent(indent) * '    ':
                    Raise(l, '3', f"'{parts[0].title()}' statment outside the function? Maybe you forgot an indent?")
                if isTake:
                    functions[-1].get('obj').params = ast_parts
                else:
                    ast.extend([INDENT(indent)] + [Keyword('gives')] + ast_parts + [EOL()])
            else:
                Raise(l, '3', f"'{parts[0].title()}' statment outside the function? Maybe you forgot an indent?")
            hooks.append('pass')
        if ast_parts:
            if hooks and hooks[-1] == 'pass':
                hooks.pop()
                continue
            else:
                ast.extend([INDENT(indent)] + ast_parts + [EOL()])
    return ast
