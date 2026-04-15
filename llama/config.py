# Configuration(구성, 설정) 파일
from pydantic settings import BaseSettings

class Settings(BaseSettings):
    openai_api_key: str

    class Config:
        