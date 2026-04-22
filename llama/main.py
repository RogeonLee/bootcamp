from contextlib import asynccontextmanager
from llama_cpp import Llama
from fastapi import FastAPI, Body, Request

SYSTEM_PROMPT = (
    "You are a concise assistant. "
    "Always reply in the same language as the user's input. "
    "Do not change the language. "
    "Do not mix languages."
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    llm = Llama(
        model_path="/Users/rogan/DEV/llama/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
        n_ctx=4096,
        n_threads=2,
        verbose=False,
        chat_format="llama-3",
    )
    app.state.llm = llm
    yield
    del llm


app = FastAPI(lifespan=lifespan)


@app.post("/chats")
def generate_chat_handler(
    request: Request,
    user_input: str = Body(..., embed=True),
):
    result = request.app.state.llm.create_chat_completion(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input},
        ],
        max_tokens=256,
        temperature=0.7,
    )
    return {"result": result["choices"][0]["message"]["content"].strip()}
