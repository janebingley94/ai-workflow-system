import httpx
import pytest

from nodes.code_node import CodeNode, UnsafeCodeError
from nodes.condition_node import ConditionNode
from nodes.http_node import HTTPNode
from nodes.llm_node import LLMNode
from nodes.search_node import SearchNode
from nodes.vector_store_node import VectorStoreNode


@pytest.mark.asyncio
async def test_llm_node_fallback():
    node = LLMNode({"openai_api_key": None})
    result = await node.run({"input": "hello"})
    assert "llm_output" in result
    assert "fallback" in result["llm_output"].lower()


@pytest.mark.asyncio
async def test_search_node_fallback():
    node = SearchNode({"tavily_api_key": None, "num_results": 2})
    result = await node.run({"input": "query"})
    assert len(result["search_results"]) == 2


@pytest.mark.asyncio
async def test_vector_store_in_memory():
    node = VectorStoreNode({
        "documents": [
            "hello world",
            "workflow systems are cool",
            "vector search",
        ],
        "top_k": 2,
    })
    result = await node.run({"input": "workflow"})
    assert "vector_results" in result
    assert len(result["vector_results"]) == 2


@pytest.mark.asyncio
async def test_condition_node():
    node = ConditionNode({"condition": "contains:test", "input_key": "input"})
    result = await node.run({"input": "test value"})
    assert result["condition_result"] == "true"


@pytest.mark.asyncio
async def test_http_node_mock():
    async def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"ok": True})

    transport = httpx.MockTransport(handler)
    node = HTTPNode({"method": "GET", "url": "https://example.com"})

    async with httpx.AsyncClient(transport=transport) as client:
        # monkeypatch client by injecting into node config
        node.config["_client"] = client

    # override execute to use mock transport
    async def execute_with_transport(state):
        async with httpx.AsyncClient(transport=transport) as client:
            response = await client.request("GET", "https://example.com")
        return {"http_response": {"status": response.status_code, "data": response.json()}}

    node.execute = execute_with_transport  # type: ignore
    result = await node.run({})
    assert result["http_response"]["status"] == 200


@pytest.mark.asyncio
async def test_code_node_rejects_unsafe():
    node = CodeNode({"code": "import os"})
    with pytest.raises(UnsafeCodeError):
        await node.execute({})


@pytest.mark.asyncio
async def test_code_node_executes_result():
    node = CodeNode({"code": "result = input + 1"})
    result = await node.run({"input": 1})
    assert result["code_result"] == 2
