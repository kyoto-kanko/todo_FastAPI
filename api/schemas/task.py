from typing import Optional

from pydantic import BaseModel, Field


# BaseModelはFastAPIのスキーマモデルであることを表すので、このクラスを継承してTaskBaseクラスを作成
class TaskBase(BaseModel):
    title: Optional[str] = Field(None)
    flag: bool = Field(False)


class TaskCreateResponse(TaskBase):
    id: int

    class Config:
        orm_mode = True


class Task(TaskBase):
    id: int

    class Config:
        orm_mode = True


class TaskEdit(BaseModel):
    title: Optional[str] = Field(None)


class TaskCheck(BaseModel):
    flag: bool = Field(True)


class TaskUnCheck(BaseModel):
    flag: bool = Field(False)
