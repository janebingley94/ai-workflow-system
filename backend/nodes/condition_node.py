from __future__ import annotations

from typing import Any, Dict

from nodes.base_node import BaseNode


class ConditionNode(BaseNode):
    async def execute(self, state: Dict[str, Any]) -> Dict[str, Any]:
        condition = str(self.config.get("condition", ""))
        input_key = self.config.get("input_key", "input")
        value = str(state.get(input_key, ""))

        result = self._evaluate_condition(condition, value)
        return {
            "condition_result": "true" if result else "false",
            "logs": [
                {
                    "node": "ConditionNode",
                    "condition": condition,
                    "input_key": input_key,
                    "result": result,
                }
            ],
        }

    def _evaluate_condition(self, condition: str, value: str) -> bool:
        if condition.startswith("contains:"):
            keyword = condition.split(":", 1)[1]
            return keyword in value
        if condition.startswith("length>"):
            try:
                limit = int(condition.split(">", 1)[1])
            except ValueError:
                return False
            return len(value) > limit
        if condition.startswith("equals:"):
            expected = condition.split(":", 1)[1]
            return value == expected
        return False
