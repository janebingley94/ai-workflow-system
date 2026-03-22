import os
import pytest
import httpx

os.environ["DATABASE_URL"] = "sqlite+aiosqlite:////tmp/ai_workflow_test.db"

from main import app  # noqa: E402


def _sample_flow() -> dict:
    return {
        "id": "wf_sample",
        "name": "Sample",
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


@pytest.mark.asyncio
async def test_workflow_crud():
    transport = httpx.ASGITransport(app=app, lifespan="on")
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        payload = {
            "name": "Test Workflow",
            "flow_config": _sample_flow(),
        }

        create_res = await client.post("/workflows", json=payload)
        assert create_res.status_code == 201
        data = create_res.json()
        workflow_id = data["id"]

        list_res = await client.get("/workflows")
        assert list_res.status_code == 200
        assert any(item["id"] == workflow_id for item in list_res.json())

        get_res = await client.get(f"/workflows/{workflow_id}")
        assert get_res.status_code == 200

        update_res = await client.put(
            f"/workflows/{workflow_id}",
            json={"name": "Updated", "flow_config": _sample_flow()},
        )
        assert update_res.status_code == 200
        assert update_res.json()["name"] == "Updated"

        delete_res = await client.delete(f"/workflows/{workflow_id}")
        assert delete_res.status_code == 204
