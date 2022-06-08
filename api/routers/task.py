from typing import List

from fastapi import APIRouter, Depends, HTTPException

import api.schemas.task as task_schema
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.task as task_crud
from api.db import get_db

from fastapi_login import LoginManager

from fastapi.security import OAuth2PasswordRequestForm

from fastapi_login.exceptions import InvalidCredentialsException


router = APIRouter()

# 秘密鍵を生成
# python3 -c "import os; print(os.urandom(24).hex())"
SECRET = "81d28a5c4202fbac6507f9f68dd6ef12b81b7a716e8a60d4"

# LoginManagerを初期化
# LoginManager(秘密鍵、トークンを生成するURL)
manager = LoginManager(SECRET, "/login")

# 疑似ユーザデータ
fake_user = {"users": {"fake": {"password": "test1234"}}}


# 返り値として{'name': 'John Doe', 'password': 'hunter2'}を返す
@manager.user_loader()
def query_user(user_id: str):
    return fake_user["users"].get(user_id)


# Todoリストの一覧表示
@router.get("/tasks", response_model=List[task_schema.Task])
async def list_tasks(
    db: AsyncSession = Depends(
        get_db,
    ),
    user=Depends(manager),
):
    return await task_crud.get_tasks(db)


# Todoリストの新規作成
@router.post("/task", response_model=task_schema.TaskCreateResponse)
async def create_task(
    task_body: task_schema.TaskBase,
    db: AsyncSession = Depends(get_db),
    user=Depends(manager),
):
    return await task_crud.create_task(db, task_body)


# Todoリストの編集
@router.put("/task/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(
    task_id: int,
    task_body: task_schema.TaskEdit,
    db: AsyncSession = Depends(get_db),
    user=Depends(manager),
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.update_task(db, task_body, original=task)


# Todoリストの削除
@router.delete("/task/{task_id}", response_model=None)
async def delete_task(
    task_id: int, db: AsyncSession = Depends(get_db), user=Depends(manager)
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.delete_task(db, original=task)


# Todoリストにチェック
@router.put("/task/{task_id}/check", response_model=task_schema.TaskCreateResponse)
async def check_task(
    task_id: int,
    task_body: task_schema.TaskCheck,
    db: AsyncSession = Depends(get_db),
    user=Depends(manager),
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.check_task(db, task_body, original=task)


# Todoリストのチェックを外す
@router.put("/task/{task_id}/uncheck", response_model=task_schema.TaskCreateResponse)
async def uncheck_task(
    task_id: int,
    task_body: task_schema.TaskUnCheck,
    db: AsyncSession = Depends(get_db),
    user=Depends(manager),
):
    task = await task_crud.get_task(db, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_crud.uncheck_task(db, task_body, original=task)


# ログインルートの作成
# OAuth2PasswordRequestFormはusernameとpasswordを取得
@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = query_user(email)
    if not user:
        # you can return any response or error of your choice
        raise InvalidCredentialsException
    elif password != user["password"]:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data={"sub": email})
    return {"access_token": access_token}


@router.get("/proteced")
def protected_route(user=Depends(manager)):
    return {"user": user}
