# https://fastapi.tiangolo.com/ja/tutorial/first-steps/
from fastapi import FastAPI

from api.routers import task, done

# FastAPIをインスタンス化
app = FastAPI()
app.include_router(task.router)
app.include_router(done.router)
