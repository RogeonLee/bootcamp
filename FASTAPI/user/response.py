# 응답 데이터의 형식 관리
# 1) 클라이언트에게 잘못된 데이터를 반환하지 않기 위해
# 2) 민감 데이터(개인정보 등)를 실수로 유출하지 않기 위해

# response.py
from datetime import datetime  # ← 추가!
from pydantic import BaseModel  # ← 추가!

class UserResponse(BaseModel):
    id: int
    name: str
    job: str
    created_at: datetime  # DB에서 자동으로 저장되는 생성 시각도 응답 데이터에 포함