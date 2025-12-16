import ast

def parse_python_code(file_path, code):
    """
    Parses Python code into functions and classes using AST.
    """
    tree = ast.parse(code)
    chunks = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            chunks.append({
                "type": "function",
                "name": node.name,
                "lineno": node.lineno,
                "code": ast.get_source_segment(code, node)
            })

        elif isinstance(node, ast.ClassDef):
            chunks.append({
                "type": "class",
                "name": node.name,
                "lineno": node.lineno,
                "code": ast.get_source_segment(code, node)
            })

    return chunks
