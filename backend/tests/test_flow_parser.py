import pytest

from engine.flow_parser import FlowParser
from models.schemas import NodeConfig


def test_flow_parser_simple_graph():
    parser = FlowParser()
    flow = {
        "id": "wf1",
        "name": "Simple",
        "nodes": [
            {"id": "input_1", "type": "input", "position": {}, "data": {"input_key": "input"}},
            {"id": "llm_1", "type": "llm", "position": {}, "data": {}},
            {"id": "output_1", "type": "output", "position": {}, "data": {}},
        ],
        "edges": [
            {"id": "e1", "source": "input_1", "target": "llm_1"},
            {"id": "e2", "source": "llm_1", "target": "output_1"},
        ],
    }

    compiled = parser.parse(flow)
    assert compiled is not None


def test_flow_parser_condition_edges_missing():
    parser = FlowParser()
    flow = {
        "id": "wf2",
        "name": "Cond",
        "nodes": [
            {"id": "input_1", "type": "input", "position": {}, "data": {}},
            {"id": "cond_1", "type": "condition", "position": {}, "data": {}},
            {"id": "llm_1", "type": "llm", "position": {}, "data": {}},
            {"id": "output_1", "type": "output", "position": {}, "data": {}},
        ],
        "edges": [
            {"id": "e1", "source": "input_1", "target": "cond_1"},
            {"id": "e2", "source": "cond_1", "target": "llm_1", "condition": "true"},
        ],
    }

    with pytest.raises(ValueError):
        parser.parse(flow)


def test_dynamic_state_fields():
    parser = FlowParser()
    flow = {
        "id": "wf3",
        "name": "State",
        "nodes": [
            {"id": "input_1", "type": "input", "position": {}, "data": {"input_key": "topic"}},
            {"id": "search_1", "type": "search", "position": {}, "data": {}},
            {"id": "vector_1", "type": "vector_store", "position": {}, "data": {}},
            {"id": "cond_1", "type": "condition", "position": {}, "data": {}},
            {"id": "http_1", "type": "http", "position": {}, "data": {}},
            {"id": "code_1", "type": "code", "position": {}, "data": {}},
            {"id": "output_1", "type": "output", "position": {}, "data": {"output_key": "final"}},
        ],
        "edges": [],
    }

    nodes = {n["id"]: NodeConfig(**n) for n in flow["nodes"]}
    state_cls = parser._create_state_class(nodes)
    annotations = state_cls.__annotations__
    assert "topic" in annotations
    assert "search_results" in annotations
    assert "vector_results" in annotations
    assert "vector_results_text" in annotations
    assert "condition_result" in annotations
    assert "http_response" in annotations
    assert "code_result" in annotations
    assert "final" in annotations
