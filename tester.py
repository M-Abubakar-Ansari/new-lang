from Parser import sourceToAst
from Transpiler import astToLines, astToPy, lineToPy
from reprStr import Print

source = """
x is 10
y is 20
fun add
    takes x y
    gives x + y
add x y
if x > 0
    display 10
"""

ast = sourceToAst(source)
lines = astToLines(ast)
lines = astToPy(lines)
print(lineToPy(lines))
