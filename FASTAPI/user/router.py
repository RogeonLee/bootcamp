from fastapi import APIRouter, Path, Query, status, HTTPException, Depends
from sqlalchemy import select, delete
from database.connection import get_async_session
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse

router = APIRouter(tags=["User"])


# GET /users
@router.get(
    "/users",
    summary="전체 사용자 목록 조회 API",
    status_code=status.HTTP_200_OK,
    response_model=list[UserResponse],
)
async def get_users_handler(
    # Depends: FastAPI에서 의존성을 자동으로 실행/주입/정리
    session=Depends(get_async_session),
):
    # statement = 구문(명령문)
    stmt = select(User)  # SELECT * FROM user;
    result = await session.execute(stmt)
    users = result.scalars().all()  # [user1, user2, user3, ...]
    return users

# GET /users/search?name=alex
# GET /users/search?job=student
# ⚠️ /users/{user_id} 보다 위에 있어야 함
@router.get(
    "/users/search",
    summary="사용자 정보 검색 API",
    response_model=list[UserResponse],
)
async def search_users_handler(
    name: str | None = Query(None),
    job: str | None = Query(None),
    session=Depends(get_async_session),
):
    if not name and not job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="검색 조건이 없습니다.",
        )

    stmt = select(User) # SELECT문을 만들어서 stmt에 담아놓음, 실제로 조회가 되는 건 아님, stmt상에서 where 조건을 붙여서 쿼리를 완성시켜야 함
    if name:
        stmt = stmt.where(User.name == name) # 쿼리문을 작성하고 있는 단계. 
    if job:
        stmt = stmt.where(User.job == job)

    result = await session.execute(stmt) # stmt에 담긴 쿼리를 DB에 전달해서 실행시키는 단계이기 때문에 여기서 await가 필요함
    users = result.scalars().all() # 가져온 데이터를 list 형태로 변환해서 users에 담아놓음
    return result.scalars().all() # users를 반환해도 되지만, result.scalars().all()을 반환해도 됨, users는 사실상 불필요한 변수임

# GET /users/{user_id}
@router.get("/users/{user_id}")
async def get_user_handler(
    user_id: int = Path(..., ge=1),
    session=Depends(get_async_session),
):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )
    return user


# POST /users
@router.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
)
async def create_user_handler(
    body: UserCreateRequest,
    session=Depends(get_async_session),
):
    new_user = User(name=body.name, job=body.job)
    session.add(new_user)
    print(new_user.id, new_user.created_at) # 아직 id, created_at이 없음 (DB에 저장되기 전이기 때문)
    await session.commit() # 변경사항 저장
    await session.refresh(new_user) # id, created_at 읽어옴
    print(new_user.id, new_user.created_at) # 이제 id, created_at이 있음
    return new_user


# PATCH /users/{user_id}
@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
)
async def update_user_handler(
    user_id: int,
    body: UserUpdateRequest,
    session=Depends(get_async_session),
):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )

    user.job = body.job
    await session.commit()
    await session.refresh(user)
    return user


# DELETE /users/{user_id}
@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_handler(
    user_id: int,
    session=Depends(get_async_session),
):
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User Not Found",
        )

    await session.delete(user)
    await session.commit()