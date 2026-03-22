from __future__ import annotations

import operator
from typing import Any, Dict, Optional, TypedDict, Annotated

from langgraph.graph import END, StateGraph

from engine.node_registry import NodeRegistry
from models.schemas import FlowConfig, NodeConfig, EdgeConfig


class FlowParser:
    def __init__(self) -> None:
        self.node_registry = NodeRegistry()

    def parse(self, flow_config: FlowConfig | dict) -> Any:
        config = flow_config
        if isinstance(flow_config, dict):
            config = FlowConfig.model_validate(flow_config)

        nodes_by_id = {node.id: node for node in config.nodes}
        edges = config.edges

        state_cls = self._create_state_class(nodes_by_id)
        workflow = StateGraph(state_cls)

        for node_id, node in nodes_by_id.items():
            if node.type in {"input", "output"}:
                continue
            node_fn = self.node_registry.get_node_function(node.type, {**node.data, "node_id": node_id})
            workflow.add_node(node_id, node_fn)

        entry_node = self._find_entry_node(nodes_by_id, edges)
        if entry_node is None:
            raise ValueError("Unable to determine entry node")
        workflow.set_entry_point(entry_node)

        output_ids = {node.id for node in nodes_by_id.values() if node.type == "output"}
        condition_sources = {node.id for node in nodes_by_id.values() if node.type == "condition"}

        for edge in edges:
            source = edge.source
            target = edge.target

            if nodes_by_id.get(source) and nodes_by_id[source].type == "input":
                continue

            if target in output_ids:
                workflow.add_edge(source, END)
                continue

            if source in condition_sources:
                continue

            workflow.add_edge(source, target)

        for condition_source in condition_sources:
            mapping = self._collect_condition_edges(condition_source, edges)
            workflow.add_conditional_edges(condition_source, self._make_condition_fn(), mapping)

        return workflow.compile()

    def _create_state_class(self, nodes: Dict[str, NodeConfig]) -> type:
        fields: Dict[str, Any] = {
            "logs": Annotated[list, operator.add],
        }

        for node in nodes.values():
            node_type = node.type
            data = node.data
            if node_type == "input":
                input_key = data.get("input_key", "input")
                fields[input_key] = str
            elif node_type == "output":
                output_key = data.get("output_key", "output")
                fields[output_key] = Optional[str]
            elif node_type == "llm":
                output_key = data.get("output_key", "llm_output")
                fields[output_key] = Optional[str]
            elif node_type == "search":
                output_key = data.get("output_key", "search_results")
                fields[output_key] = list
            elif node_type == "vector_store":
                output_key = data.get("output_key", "vector_results")
                fields[output_key] = list
                fields["vector_results_text"] = Optional[str]
            elif node_type == "condition":
                fields["condition_result"] = Optional[str]
            elif node_type == "http":
                output_key = data.get("output_key", "http_response")
                fields[output_key] = dict
            elif node_type == "code":
                output_key = data.get("output_key", "code_result")
                fields[output_key] = Any

        return TypedDict("WorkflowState", fields, total=False)

    def _find_entry_node(
        self,
        nodes: Dict[str, NodeConfig],
        edges: list[EdgeConfig],
    ) -> str | None:
        input_nodes = {node.id for node in nodes.values() if node.type == "input"}
        if input_nodes:
            for edge in edges:
                if edge.source in input_nodes:
                    return edge.target

        incoming: Dict[str, int] = {node_id: 0 for node_id in nodes.keys()}
        for edge in edges:
            incoming[edge.target] = incoming.get(edge.target, 0) + 1

        candidates = [
            node_id
            for node_id, count in incoming.items()
            if count == 0 and nodes[node_id].type != "output"
        ]
        if candidates:
            return candidates[0]

        for node_id, node in nodes.items():
            if node.type != "output":
                return node_id

        return None

    def _collect_condition_edges(
        self,
        source: str,
        edges: list[EdgeConfig],
    ) -> Dict[str, str]:
        mapping: Dict[str, str] = {}
        for edge in edges:
            if edge.source != source:
                continue
            if edge.condition:
                mapping[edge.condition] = edge.target

        if "true" not in mapping or "false" not in mapping:
            raise ValueError(f"Condition node '{source}' missing true/false edges")
        return mapping

    def _make_condition_fn(self):
        def condition_fn(state: Dict[str, Any]) -> str:
            value = str(state.get("condition_result", "false")).lower()
            return "true" if value == "true" else "false"

        return condition_fn
