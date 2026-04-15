from contextlib import asynccontextmanager
from llama_cpp import Llama
from fastapi import FastAPI, Body, Depends, Request
from fastapi.responses import StreamingResponse
from openai import OpenAI
from config import Settings

settings = Settings()

SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.llm = Llama(
        model_path="/Users/rogan/DEV/llama/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        n_ctx=4096,
        n_threads=2,
        verbose=False,
        chat_format="llama-3",
    )
    app.state.openai_client = OpenAI(api_key=settings.openai_api_key)
    yield

app = FastAPI(lifespan=lifespan)

def get_llm(request: Request):
    return request.app.state.llm

def get_openai_client(request: Request):
    return request.app.state.openai_client

@app.post("/chats")
async def generate_chat_handler(
    user_input: str = Body(..., embed=True),
    llm=Depends(get_llm),
):
    async def event_generator():
        result = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            max_tokens=256,
            temperature=0.7,
            stream=True,
        )
        for chunk in result:
            token = chunk["choices"][0]["delta"].get("content")
            if token:
                yield token

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )

# generate_chat_handler 함수는 POST 요청을 처리하는 FastAPI 엔드포인트입니다.
# 이 함수는 사용자 입력을 받아 Llama 모델을 사용하여 채팅 응답을 생성합니다. 
# 응답은 스트리밍 방식으로 클라이언트에 전송됩니다. 
# 사용자 입력은 JSON 본문에서 "user_input" 필드로 전달되며, Llama 모델은 시스템 프롬프트와 사용자 입력을 기반으로 응답을 생성합니다. 
# 생성된 응답은 토큰 단위로 스트리밍되어 클라이언트에 전송됩니다.   

# --- OpenAI 엔드포인트 (스트리밍) ---
@app.post("/openai")
async def openai_handler(
    user_input: str = Body(..., embed=True),
    openai_client=Depends(get_openai_client),
):
    async def event_generator():
        async with openai_client.responses.stream(
            model="gpt-4.1-mini",
            input=user_input,
            text_format=OpenAIResponse,
        ) as stream:
            async for event in stream:
                # 텍스트 토큰
                if event.type == "response.output_text.delta":
                    yield event.data

                # 연결 종료
                elif event.type == "response.completed":
                    break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )