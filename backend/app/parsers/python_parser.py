import ast
from typing import Dict, List, Any

class PythonASTParser:
    def __init__(self, source_code: str, filepath: str):
        self.source_code = source_code
        self.filepath = filepath
        self.tree = None
        try:
            self.tree = ast.parse(source_code)
        except SyntaxError as e:
            self.error = str(e)

    def parse(self) -> Dict[str, Any]:
        if not self.tree:
            return {"error": getattr(self, "error", "Unknown parse error")}

        result = {
            "imports": [],
            "classes": [],
            "functions": [],
            "calls": [],
            "line_count": len(self.source_code.splitlines())
        }

        # First pass: find all classes and functions
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    result["imports"].append({
                        "type": "import",
                        "module": alias.name,
                        "line": node.lineno
                    })
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for alias in node.names:
                        result["imports"].append({
                            "type": "import_from",
                            "module": node.module,
                            "name": alias.name,
                            "line": node.lineno
                        })
            elif isinstance(node, ast.ClassDef):
                class_info = self._parse_class(node)
                result["classes"].append(class_info)
            elif isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                # Only add top-level functions here. Methods are handled inside classes.
                # However, ast.walk yields all nodes. We can filter out methods later or check parent.
                # Since ast doesn't have parent pointers by default, we'll extract all and organize later,
                # or just add parent tracking.
                pass
            elif isinstance(node, ast.Call):
                call_info = self._parse_call(node)
                if call_info:
                    result["calls"].append(call_info)

        # Better approach: Add parent pointers
        for node in ast.walk(self.tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node

        # Extract top-level functions and methods
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_info = self._parse_function(node)
                parent = getattr(node, "parent", None)
                if isinstance(parent, ast.ClassDef):
                    # It's a method, already added in class parsing if we do it there,
                    # but let's just make it flat with a class reference.
                    func_info["class_name"] = parent.name
                    func_info["is_method"] = True
                else:
                    func_info["is_method"] = False
                result["functions"].append(func_info)

        return result

    def _parse_class(self, node: ast.ClassDef) -> Dict[str, Any]:
        bases = []
        for base in node.bases:
            if isinstance(base, ast.Name):
                bases.append(base.id)
            elif isinstance(base, ast.Attribute):
                bases.append(base.attr)
        
        return {
            "name": node.name,
            "start_line": node.lineno,
            "end_line": getattr(node, "end_lineno", node.lineno),
            "docstring": ast.get_docstring(node),
            "inherits": bases
        }

    def _parse_function(self, node: ast.AST) -> Dict[str, Any]:
        decorators = []
        for dec in node.decorator_list:
            if isinstance(dec, ast.Name):
                decorators.append(dec.id)
            elif isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                # e.g. @app.get("/users")
                decorators.append(f"{dec.func.value.id}.{dec.func.attr}" if isinstance(dec.func.value, ast.Name) else dec.func.attr)

        # Check for endpoints
        is_endpoint = False
        endpoint_path = None
        endpoint_method = None
        
        for dec in node.decorator_list:
            if isinstance(dec, ast.Call) and isinstance(dec.func, ast.Attribute):
                method_name = dec.func.attr.upper()
                if method_name in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
                    is_endpoint = True
                    endpoint_method = method_name
                    if dec.args and isinstance(dec.args[0], ast.Constant):
                        endpoint_path = dec.args[0].value

        return {
            "name": node.name,
            "start_line": node.lineno,
            "end_line": getattr(node, "end_lineno", node.lineno),
            "docstring": ast.get_docstring(node),
            "decorators": decorators,
            "is_endpoint": is_endpoint,
            "endpoint_method": endpoint_method,
            "endpoint_path": endpoint_path,
            "is_async": isinstance(node, ast.AsyncFunctionDef)
        }

    def _parse_call(self, node: ast.Call) -> Dict[str, Any]:
        func_name = None
        if isinstance(node.func, ast.Name):
            func_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            func_name = node.func.attr
        
        if func_name:
            return {
                "name": func_name,
                "line": node.lineno
            }
        return None

if __name__ == "__main__":
    sample_code = """
import os
from fastapi import FastAPI

app = FastAPI()

class User:
    def __init__(self):
        pass

@app.get("/users")
def get_users():
    return User()
"""
    parser = PythonASTParser(sample_code, "test.py")
    import json
    print(json.dumps(parser.parse(), indent=2))
