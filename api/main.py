# https://fastapi.tiangolo.com/ja/tutorial/first-steps/
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.routers import task, done

# FastAPIをインスタンス化
app = FastAPI()

# CORS回避
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(task.router)
app.include_router(done.router)
