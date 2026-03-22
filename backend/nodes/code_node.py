from __future__ import annotations

import ast
from typing import Any, Dict

from nodes.base_node import BaseNode


class UnsafeCodeError(ValueError):
    pass


class CodeNode(BaseNode):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        code = str(self.config.get("code", ""))
        output_key = self.config.get("output_key", "code_result")
        inputs = self.config.get("inputs") or {}

        tree = ast.parse(code, mode="exec")
        self._validate_ast(tree)

        safe_builtins = {
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "len": len,
            "range": range,
            "enumerate": enumerate,
            "sorted": sorted,
            "round": round,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
        }

        exec_globals = {"__builtins__": safe_builtins}
        exec_locals: Dict[str, Any] = {
            **state,
            **inputs,
        }

        compiled = compile(tree, filename="<code_node>", mode="exec")
        exec(compiled, exec_globals, exec_locals)

        if "outputs" in exec_locals and isinstance(exec_locals["outputs"], dict):
            outputs = exec_locals["outputs"]
            return {
                **outputs,
                "logs": [
                    {
                        "node": "CodeNode",
                        "mode": "outputs",
                    }
                ],
            }

        result = exec_locals.get("result")
        return {
            output_key: result,
            "logs": [
                {
                    "node": "CodeNode",
                    "mode": "result",
                }
            ],
        }

    def _validate_ast(self, tree: ast.AST) -> None:
        banned_calls = {"eval", "exec", "open", "__import__", "compile", "input"}
        banned_nodes = (ast.Import, ast.ImportFrom, ast.Global, ast.Nonlocal, ast.With)

        for node in ast.walk(tree):
            if isinstance(node, banned_nodes):
                raise UnsafeCodeError("Unsafe statement detected")

            if isinstance(node, ast.Attribute):
                if node.attr.startswith("__"):
                    raise UnsafeCodeError("Dunder access is not allowed")

            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name) and node.func.id in banned_calls:
                    raise UnsafeCodeError("Unsafe function call detected")
