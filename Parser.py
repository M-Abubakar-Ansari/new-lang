# PARSER
import string as st
from astSource import *
from Builtins import lang_builtins, prefix
import math
from Error import Raise

def Indent(spaces, tabsize=4):
    tabs = math.ceil(spaces / tabsize)
    return tabs

letters = st.ascii_letters
digits = st.digits
functions = []
isi = isinstance

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
            elif i.isspace() or i == ',':
                if word:
                    parts.append(word)
                    word = ''
                if i == ',':
                    parts.append(',')
            else:
                word += i
    if word:
        parts.append(word)
    return parts

def exprToAst(expr: str):
    tokens = _filter_strings_and_identifiers(expr)
    final_tokens = []
    current_expr = []
    
    for t in tokens:
        if t.startswith('"') and t.endswith('"'):
            if current_expr:
                final_tokens.extend(current_expr)
                current_expr = []
            final_tokens.append(t)
        elif t == ',':
            if current_expr:
                final_tokens.extend(current_expr)
                current_expr = []
            final_tokens.append(SEP())
        else:
            current_expr.append(t)
    
    if current_expr:
        final_tokens.extend(current_expr)

    # Build AST with function call nesting
    ast = []
    i = 0
    while i < len(final_tokens):
        t = final_tokens[i]
        if isinstance(t, str):
            if t.startswith('"') and t.endswith('"'):
                ast.append(string(t[1:-1]))
            elif t.replace('.', '', 1).isdigit():
                ast.append(num(t))
            elif t in operators:
                ast.append(Operator(t))
            elif t in keywords:
                ast.append(Keyword(t))
            elif t in [f.get('obj').name for f in functions] or t in lang_builtins:
                name = t if t not in lang_builtins else t
                args = []
                current_arg = []
                i += 1
                while i < len(final_tokens):
                    if final_tokens[i] == SEP():
                        if current_arg:
                            arg_ast = exprToAst(' '.join(str(x) for x in current_arg))
                            args.extend(arg_ast)
                            args.append(SEP())
                        current_arg = []
                    else:
                        current_arg.append(final_tokens[i])
                    i += 1
                    if i >= len(final_tokens):
                        break
                
                if current_arg:
                    arg_ast = exprToAst(' '.join(str(x) for x in current_arg))
                    args.extend(arg_ast)
                
                i -= 1
                ast.append(FunctionCall(name, args))
            else:
                ast.append(Identifier(t))
        elif isinstance(t, SEP):
            ast.append(t)
        else:
            ast.append(t)
        i += 1
    
    return ast

def variableToAst(expr):
    expr = str(expr).split('is', 1)
    if len(expr) < 2:
        Raise(expr, '3', "Variable assignment missing 'is' keyword.")
    name, value = expr[0].strip(), expr[1].strip()
    return [Identifier(name), Keyword('is'), *(exprToAst(value))]

def functionToAst(expr):
    parts = str(expr).split()
    if len(parts) < 2:
        Raise(expr, '3', "Function definition missing a name.")
    name = parts[1]
    return [FunctionDef(name)]

def sourceToAst(source):
    source = str(source).splitlines()
    ast = []
    for l in source:
        l = l.rstrip()
        if not l: continue
        indent = Indent(len(l) - len(l.lstrip()))
        stripped_l = l.strip()
        parts = _filter_strings_and_identifiers(stripped_l)
        
        ast_parts = None
        if len(parts) > 2 and parts[1] == 'is':
            ast_parts = variableToAst(stripped_l)
        elif parts and parts[0] in ['if', 'elif', 'else']:
            cond_str = stripped_l.removeprefix(parts[0]).strip()
            if cond_str.endswith('?'):
                cond_str = cond_str[:-1].strip()
            ast_parts = [Conditional(exprToAst(cond_str), parts[0])]
        elif parts and parts[0] == 'fun':
            ast_parts = functionToAst(stripped_l)
            indent_node = INDENT(indent)
            line_ast = [indent_node] + ast_parts + [EOL()]
            ast.extend(line_ast)
            functions.append({'obj': ast_parts[0], 'ind': len(ast) - len(line_ast)})
            continue # Skip adding EOL again
        elif parts and parts[0] in ['takes', 'gives']:
            if not functions:
                Raise(l, '3', f"'{parts[0].title()}' statement outside a function. Maybe you forgot an indent?")
            
            isTake = parts[0] == 'takes'
            if isTake:
                params_str = stripped_l.removeprefix('takes').strip()
                params = []
                if params_str:
                    for param in params_str.split(','):
                        param = param.strip()
                        if param:
                            params.append(Identifier(param))
                functions[-1]['obj'].params = params
            else: # gives
                ast_parts = exprToAst(stripped_l.removeprefix('gives').strip())
            
            if ast_parts:
                ast.extend([INDENT(indent)] + [Keyword('gives')] + ast_parts + [EOL()])
            continue # Skip adding EOL again
        else:
            ast_parts = exprToAst(stripped_l)
        
        if ast_parts:
            ast.extend([INDENT(indent)] + ast_parts + [EOL()])
    return ast