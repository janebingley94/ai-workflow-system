from __future__ import annotations

import uuid
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_session
from engine.workflow_runner import run_workflow_in_background
from models.database import Workflow
from models.schemas import ExecuteRequest, ExecuteResponse, WorkflowCreate, WorkflowOut, WorkflowUpdate

router = APIRouter(prefix="/workflows", tags=["workflows"])


@router.get("", response_model=List[WorkflowOut])
async def list_workflows(session: AsyncSession = Depends(get_session)) -> List[WorkflowOut]:
    result = await session.execute(select(Workflow).order_by(Workflow.created_at.desc()))
    workflows = result.scalars().all()
    return workflows


@router.get("/{workflow_id}", response_model=WorkflowOut)
async def get_workflow(workflow_id: str, session: AsyncSession = Depends(get_session)) -> WorkflowOut:
    workflow = await session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.post("", response_model=WorkflowOut, status_code=201)
async def create_workflow(
    payload: WorkflowCreate,
    session: AsyncSession = Depends(get_session),
) -> WorkflowOut:
    workflow = Workflow(name=payload.name, flow_config=payload.flow_config.model_dump())
    session.add(workflow)
    await session.commit()
    await session.refresh(workflow)
    return workflow


@router.put("/{workflow_id}", response_model=WorkflowOut)
async def update_workflow(
    workflow_id: str,
    payload: WorkflowUpdate,
    session: AsyncSession = Depends(get_session),
) -> WorkflowOut:
    workflow = await session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    if payload.name is not None:
        workflow.name = payload.name
    if payload.flow_config is not None:
        workflow.flow_config = payload.flow_config.model_dump()

    await session.commit()
    await session.refresh(workflow)
    return workflow


@router.delete("/{workflow_id}", status_code=204)
async def delete_workflow(workflow_id: str, session: AsyncSession = Depends(get_session)) -> None:
    workflow = await session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    await session.delete(workflow)
    await session.commit()


@router.post("/{workflow_id}/execute", response_model=ExecuteResponse)
async def execute_workflow(
    workflow_id: str,
    payload: ExecuteRequest,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
) -> ExecuteResponse:
    workflow = await session.get(Workflow, workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    execution_id = str(uuid.uuid4())
    background_tasks.add_task(run_workflow_in_background, execution_id, workflow.flow_config, payload.input)

    return ExecuteResponse(execution_id=execution_id)
