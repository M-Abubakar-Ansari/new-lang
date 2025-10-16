import unittest
from Parser import sourceToAst
from Transpiler import astToLines, astToPy, lineToPy, run
import io
import sys
from contextlib import contextmanager

@contextmanager
def capture_stdout():
    """Capture stdout for testing"""
    new_out = io.StringIO()
    old_out = sys.stdout
    try:
        sys.stdout = new_out
        yield new_out
    finally:
        sys.stdout = old_out

class LanguageTests(unittest.TestCase):
    def transpile_and_run(self, source):
        """Helper to transpile and run code, returns (output, generated_code)"""
        ast = sourceToAst(source)
        lines = astToLines(ast)
        py_lines = astToPy(lines)
        code = lineToPy(py_lines)
        with capture_stdout() as out:
            run('from Builtins import *\n' + code)
        return out.getvalue().strip(), code

    def test_basic_assignment(self):
        source = """
x is 10
display x
"""
        output, code = self.transpile_and_run(source)
        self.assertEqual(output, "10")
        self.assertIn("py_py__x = 10", code)

    def test_function_definition_and_call(self):
        source = """
fun add
    takes x, y
    gives x + y
z is add 5, 3
display z
"""
        output, code = self.transpile_and_run(source)
        self.assertEqual(output, "8")
        self.assertIn("def py_py__add", code)
        self.assertIn("return py_py__x + py_py__y", code)

    def test_conditional_with_function_call(self):
        source = """
x is 10
if x > 5
    display 1
else
    display 0
"""
        output, code = self.transpile_and_run(source)
        self.assertEqual(output, "1")
        self.assertIn("if py_py__x > 5:", code)

    def test_multiple_function_args(self):
        source = """
display 1+2, "hello", 3-1
"""
        output, code = self.transpile_and_run(source)
        self.assertEqual(output, "3 hello 2")
        self.assertIn("py_py__display(1 + 2, \"hello\", 3 - 1)", code)

    def test_nested_function_calls(self):
        source = """
fun double
    takes x
    gives x + x

fun add
    takes x, y
    gives x + y

display add double 2, double 3
"""
        output, code = self.transpile_and_run(source)
        self.assertEqual(output, "10")

    def test_operator_precedence(self):
        source = """
display 2 + 3 * 4
"""
        output, code = self.transpile_and_run(source)
        self.assertEqual(output, "14")

    def test_string_with_commas(self):
        source = """
display "hello, world", 123
"""
        output, code = self.transpile_and_run(source)
        self.assertEqual(output, "hello, world 123")

    def test_complex_expression(self):
        source = """
fun calc
    takes x, y
    gives x * y + 2

a is 5
b is 3
display calc a, b
"""
        output, code = self.transpile_and_run(source)
        self.assertEqual(output, "17")

if __name__ == '__main__':
    unittest.main()