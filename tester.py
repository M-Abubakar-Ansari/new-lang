from Parser import sourceToAst
from Transpiler import astToLines
from reprStr import Print

source = """
fun add:
    takes x y=0 z=0
    gives xy + y + z
x is 10
y is 20
gives is add x y x+y
if xy > 0?
    ...
"""

ast = sourceToAst(source)
lines = astToLines(ast)
lines = [str(i) for i in lines]
Print('\n'.join(lines))
