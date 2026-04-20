from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "mysql+pymysql://root:password@db:3306/app_db"

engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionFactory = sessionmaker(
    bind=engine, class_=AsyncSession, autocommit=False, autoflush=False, expire_on_commit=False
)


Base.metadata.create_all(bind=engine)