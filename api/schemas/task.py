from typing import Optional

from pydantic import BaseModel, Field


# BaseModelはFastAPIのスキーマモデルであることを表すので、このクラスを継承してTaskBaseクラスを作成
class TaskBase(BaseModel):
    title: Optional[str] = Field(None)


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    id: int

    class Config:
        orm_mode = True


class Task(TaskBase):
    id: int
    done: bool = Field(False, description="完了フラグ")

    class Config:
        orm_mode = True
