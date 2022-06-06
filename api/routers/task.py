from typing import List

from fastapi import APIRouter, Depends, HTTPException

import api.schemas.task as task_schema
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.task as task_crud
from api.db import get_db


router = APIRouter()


# Todoリストの一覧表示
@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(db: AsyncSession = Depends(get_db)):
    return await task_crud.get_tasks(db)


# Todoリストの新規作成
@router.post("/task", response_model=task_schema.TaskCreateResponse)
async def create_task(
    task_body: task_schema.TaskBase, db: AsyncSession = Depends(get_db)
):
    return await task_crud.create_task(db, task_body)


# Todoリストの編集
@router.put("/task/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int, task_body: task_schema.TaskEdit, db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.update_task(db, task_body, original=task)


# Todoリストの削除
@router.delete("/task/{task_id}", response_model=None)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)


# Todoリストにチェック
@router.put("/task/{task_id}/check", response_model=task_schema.TaskCreateResponse)
async def check_task(
    task_id: int, task_body: task_schema.TaskCheck, db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.check_task(db, task_body, original=task)


# Todoリストのチェックを外す
@router.put("/task/{task_id}/uncheck", response_model=task_schema.TaskCreateResponse)
async def uncheck_task(
    task_id: int, task_body: task_schema.TaskUnCheck, db: AsyncSession = Depends(get_db)
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.uncheck_task(db, task_body, original=task)
