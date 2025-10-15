from Parser import sourceToAst
from Transpiler import astToLines
from reprStr import Print

source = """
x is 10
y is 20
fun add
    takes x y
    gives x + y
add x y
"""

ast = sourceToAst(source)
lines = astToLines(ast)
lines = [str(i) for i in lines]
Print('\n'.join(lines))
