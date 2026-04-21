from fastapi import APIRouter, status, Depends, HTTPException  
# Depends는 중복 코드를 줄여 코드를 더 깔끔하게 만들어주는 FastAPI의 기능입니다. 의존성 주입을 통해 필요한 리소스를 자동으로 제공받을 수 있습니다.
from sqlalchemy import select
from database.connection import get_session, AsyncSessionFactory, engine, AsyncSession, create_async_engine, async_sessionmaker, DATABASE_URL, get_session, 

from user.request import SignupRequest, LoginRequest, LoginResponse, SignupResponse
from user.models import User, Base, init_db

router = APIRouter(tags=["User"])

@router.post(
    "/users",
    summary="회원가입 API",
    status_code=status.HTTP_201_CREATED,
)
async def signup_handler(
    body: SignupRequest,
    session = Depends(get_session), # connection.py에서 정의한 get_session 함수를 의존성 주입하여 데이터베이스 세션을 가져옵니다.
):
    
    # 1) 데이터 입력(email, password)
    # 2) email 중복 체크 -> 이미 DB에 저장된 회원 데이터 중 해당 이메일로 가입한 사람이 이미 있는지 확인
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar_one_or_none() # 결과에서 하나의 User 객체를 반환하거나, 결과가 없으면 None을 반환합니다.
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 가입된 이메일입니다."
        )
    
    # 3) password 해싱(암호화)



    # 4) DB에 회원 데이터 저장
    return {"message": "회원가입 API"}

@router.post(
    "/users/login",
    summary="로그인 API",
    status_code=status.HTTP_200_OK,
)
async def login_handler(
    body: SignupRequest,
    session = Depends(get_session),
):    
    # 1) 데이터 입력(email, password)
    # 2) email로 회원 데이터 조회 -> DB에서 해당 이메일로 가입한 회원 데이터를 조회합니다.
    stmt = select(User).where(User.email == body.email)
    result = await session.execute(stmt)
    user = result.scalar()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="가입된 이메일이 없습니다."
        )



    # 3) body.password 검증 -> 입력된 비밀번호가 DB에 저장된 해시된 비밀번호와 일치하는지 확인합니다.
    verify_password = body.password == user.password # 실제로는 해시된 비밀번호를 비교해야 합니다. 이 부분은 예시이므로 단순 비교로 작성되어 있습니다.
    if not verify_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="비밀번호가 일치하지 않습니다."
        )
    
    # 4) JWT 토큰 발급 -> 로그인 성공 시, JWT 토큰을 생성하여 반환합니다.
    return {"message": "로그인 API"}