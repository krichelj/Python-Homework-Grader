import ast
import inspect
import textwrap


def uses_loop(function):
    loop_statements = ast.For, ast.While, ast.AsyncFor
    source = textwrap.dedent(inspect.getsource(function))
    function_ast = ast.parse(source)
    nodes = ast.walk(function_ast)

    return any(isinstance(node, loop_statements) for node in nodes)
