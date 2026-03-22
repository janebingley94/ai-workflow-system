from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, Type

from nodes.base_node import BaseNode
from nodes.code_node import CodeNode
from nodes.condition_node import ConditionNode
from nodes.http_node import HTTPNode
from nodes.llm_node import LLMNode
from nodes.search_node import SearchNode
from nodes.vector_store_node import VectorStoreNode

NodeCallable = Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]


class NodeRegistry:
    def __init__(self) -> None:
        self._registry: Dict[str, Type[BaseNode]] = {
            "llm": LLMNode,
            "search": SearchNode,
            "vector_store": VectorStoreNode,
            "condition": ConditionNode,
            "http": HTTPNode,
            "code": CodeNode,
        }

    def register(self, node_type: str, node_cls: Type[BaseNode]) -> None:
        self._registry[node_type] = node_cls

    def get_node_function(self, node_type: str, config: Dict[str, Any]) -> NodeCallable:
        if node_type not in self._registry:
            raise ValueError(f"Unknown node type: {node_type}")
        node = self._registry[node_type](config)
        return node.run
