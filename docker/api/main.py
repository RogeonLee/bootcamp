import uuid
import json

from fastapi import FastAPI, Body, HTTPException
from fastapi.responses import StreamingResponse
from redis import asyncio as aredis
from sqlalchemy import select

from connection_async import AsyncSessionFactory
from models import Conversation, Message


redis_client = aredis.from_url("redis://redis:6379", decode_responses=True)

app = FastAPI()


@app.post(
    "/conversations",
    summary="대화 시작 API",
)
async def create_conversation_handler():
    async with AsyncSessionFactory() as session:
        conversation = Conversation()
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
    return conversation

@app.get(
    "/conversations/{conversation_id}/messages",
    summary="전체 메세지 조회 API"
)
async def get_messages_handler(
    conversation_id: str
):
    async with AsyncSessionFactory() as session:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.id.asc())
        )
        result = await session.execute(stmt)
        messages = result.scalars().all()
    return messages

@app.post(
    "/conversations/{conversation_id}/messages",
    summary="메세지 생성 API",
)
async def create_message_handler(
    conversation_id: str,
    user_input: str = Body(..., embed=True),
):
    async with AsyncSessionFactory() as session:
        # 1) 대화방 확인
        conversation = await session.get(Conversation, conversation_id)
        if not conversation:
            raise HTTPException(
                status_code=404, detail="Conversation Not Found"
            )
        
        # 2) 사용자 메시지 생성
        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=user_input,
        )
        session.add(user_msg)

        # 3) 이전 대화내역 조회
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.id.asc()) # id 기준 오름차순
        )
        result = await session.execute(stmt)
        messages = result.scalars().all()

        # Context Rot 방지
        # 1) message 개수가 N개 이상되면, 요약해서 저장
        # 2) 대화 내역 중에 주제가 바뀌면, 이전 메시지는 무시

        history = [
            {"role": m.role, "content": m.content} for m in messages
        ]
        
        # 4) 작업 내용을 Enqueue
        channel = conversation.id
        pubsub = redis_client.pubsub()
        await pubsub.subscribe(channel)

        task = {"channel": channel, "messages": history}
        await redis_client.lpush("queue", json.dumps(task))

        await session.commit()
    
    async def event_listener():
        assistant_text = ""

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue
            
            token = message["data"]
            if token == "[DONE]":
                break

            assistant_text += token
            yield token

        # LLM 응답 메시지 저장
        async with AsyncSessionFactory() as session:
            assistant_msg = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=assistant_text
            )
            session.add(assistant_msg)
            await session.commit()
        
        await pubsub.unsubscribe(channel)
        await pubsub.close()

    return StreamingResponse(
        event_listener(),
        media_type="text/event-stream",
    )
    
#     [목표]
# - LLM과의 대화를 유지한다.
# - 이전까지는 단발성으로 사용자 입력을 Llama가 추론하는 것에 그쳤다면, 이제는 대화형으로 발전시켜보는 것.
# - 한계1: Llama는 추론을 동시에 못한다.
# - 한계2: 여러 요청을 처리할 수 없다.
# - 해결책: Redis(큐)와 worker를 여러개 띄워서 해결
# - 이 또한 스트리밍이라 저장을 하면서 보내야 하는데, 저장은 MySQL, 스트리밍은 Redis Pub/Sub으로 구현
# - FastAPI 엔드포인트 구현: /chats POST
# - 입력: user_input (사용자 메시지), conversation_id (선택적, 대화 ID)
# - 출력: 모델 추론 결과를 토큰 단위로 스트리밍
# - 데이터베이스 모델: Conversation, Message
# - Redis 사용: 작업 큐 (list), Pub/Sub (채널)