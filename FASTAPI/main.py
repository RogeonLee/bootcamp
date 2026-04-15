import anyio
from contextlib import asynccontextmanager
from starlette.concurrency import run_in_threadpool

from fastapi import FastAPI, status
from pydantic import BaseModel
from user.router import router
from database.orm import Base
from database.connection import async_engine


# 쓰레드 풀 크기 조정
@asynccontextmanager
async def lifespan(_):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_tokens = 200
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)

# 앱 시작 시 DB 테이블 자동 생성
# Base.metadata.create_all은 비동기 전환 후 별도 처리 필요

# 전역 사용자 데이터 (임시 DB 역할)
users = [
    {"id": 1, "name": "Alice", "job": "developer"},
    {"id": 2, "name": "Bob", "job": "designer"},
    {"id": 3, "name": "Charlie", "job": "manager"},
]


# 요청 본문 모델
class UserCreateRequest(BaseModel):
    name: str
    job: str


@app.get("/", status_code=200)
def root_handler():
    return {"ping": "pong"}


@app.get("/hello", status_code=status.HTTP_200_OK)
def hello_handler():
    return {"message": "Hello, FastAPI!"}


# ──────────────────────────────────────────────
# 🆕 강의: 동기 함수를 비동기 핸들러에서 사용하기
# ──────────────────────────────────────────────

def aws_sync():
    # AWS 서버랑 통신(예: 2초)
    # 비동기를 지원하지 않는 라이브러리 (boto3 등)
    return


@app.get("/async")
async def async_handler():
    # 비동기 라이브러리를 지원하지 않는 경우
    # run_in_threadpool: 동기 함수를 별도 스레드에서 실행
    # → 이벤트 루프를 블로킹하지 않음!
    await run_in_threadpool(aws_sync)
    return {"msg": "ok"}