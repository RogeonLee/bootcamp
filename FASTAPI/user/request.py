# 요청 본문의 데이터 형식 관리
from pydantic import BaseModel, Field


# 사용자 추가할 때 클라이언트가 서버에 넘겨야 하는 형식으로 UserCreateRequest 모델 정의
class UserCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=10)
    job: str

    # name: str
    # job: str  

# 사용자 데이터를 수정할 때 데이터 형식
class UserUpdateRequest(BaseModel):
    job: str

    # router 에 가서 임포트 하기 (UserUpdateRequest 추가하기)