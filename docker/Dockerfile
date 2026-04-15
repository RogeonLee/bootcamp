FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install "fastapi[standard]" # RUN은 여러개 설치할 수 있음
# 잘못된 예 — 따옴표가 스마트쿼트이거나, 쉼표 뒤 공백 문제 등

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# CMD는 하나만 사용할 수 있음. 여러개 사용하면 마지막 CMD만 실행됨. 
#그래서 RUN으로 여러개 설치하고 CMD로 실행하는 명령어 하나만 작성해야 함. docker build . 실행시 CMD는 실행되지 않음. docker run -p 8000:8000 <이미지 이름> 명령어로 실행해야 CMD가 실행됨.
# image id 앞자리 3자리로 이름 지정.
