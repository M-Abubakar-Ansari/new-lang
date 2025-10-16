import unittest
import io
import contextlib

from Parser import sourceToAst
from Transpiler import astToLines, astToPy, lineToPy

def transpile_code(source: str):
    ast = sourceToAst(source)
    lines = astToLines(ast)
    py_lines = astToPy(lines)
    code = lineToPy(py_lines)
    return code

def exec_with_builtins(code: str):
    """
    Execute generated code with Builtins imported and capture stdout.
    Returns (stdout_str, globals_dict)
    """
    buf = io.StringIO()
    g = {}
    with contextlib.redirect_stdout(buf):
        exec('from Builtins import *\n' + code, g)
    return buf.getvalue().replace('\r\n', '\n'), g

class TranspilerIntegrationTests(unittest.TestCase):
    def run_and_capture(self, source):
        code = transpile_code(source)
        out, g = exec_with_builtins(code)
        return out, code, g

    def test_assignment_and_function_call(self):
        src = """
x is 10
y is 20
fun add
    takes x y
    gives x + y
d is add x y
display d
"""
        out, code, _ = self.run_and_capture(src)
        self.assertIn('display', code)  # ensure display present in generated code
        self.assertEqual(out, "30\n")

    def test_if_else_basic(self):
        src = """
x is -5
if x > 0
    display 1
else
    display 0
"""
        out, code, _ = self.run_and_capture(src)
        # ensure conditional emitted with colon
        self.assertIn('if ', code)
        self.assertIn(':', code)
        self.assertEqual(out, "0\n")

    def test_if_elif_else(self):
        src = """
x is 0
if x > 0
    display 1
elif x = 0
    display 0
else
    display -1
"""
        out, code, _ = self.run_and_capture(src)
        # check generated code contains elif/else and colons
        self.assertTrue('elif' in code or 'elif' in code.lower())
        self.assertEqual(out, "0\n")

    def test_function_in_condition(self):
        src = """
fun is_positive
    takes n
    gives n > 0
x is 5
if is_positive x
    display "yes"
else
    display "no"
"""
        out, code, _ = self.run_and_capture(src)
        self.assertIn('is_positive', code)
        self.assertEqual(out, "yes\n")

    def test_expressions_with_function_calls(self):
        src = """
fun add
    takes a b
    gives a + b
z is add 1 2
display z
display z + 3
"""
        out, code, _ = self.run_and_capture(src)
        # should print 3 then 6
        self.assertEqual(out.splitlines(), ["3", "6"])

    def test_undefined_variable_raises_nameerror(self):
        # calling display d without defining d should raise NameError when executed
        src = """
display d
"""
        code = transpile_code(src)
        # executing should raise NameError
        with self.assertRaises(NameError):
            exec('from Builtins import *\n' + code, {})

    def test_nested_conditionals(self):
        src = """
x is 10
if x > 0
    if x > 5
        display "big"
    else
        display "small"
else
    display "none"
"""
        out, code, _ = self.run_and_capture(src)
        self.assertEqual(out, "big\n")

    def test_builtin_display_and_types(self):
        src = """
s is "hello"
n is 42
display s
display n
"""
        out, code, _ = self.run_and_capture(src)
        self.assertEqual(out.splitlines(), ["hello", "42"])

if __name__ == "__main__":
    unittest.main()