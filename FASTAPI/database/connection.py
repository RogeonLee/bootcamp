from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

DATABASE_URL = "sqlite+aiosqlite:///./local.db"

async_engine = create_async_engine(DATABASE_URL, echo=True)

SessionFactory = sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_async_session():
    async with SessionFactory() as session:
        yield session