import jwt
from datetime import datetime, timezone, timedelta

payload = {
    "exp": datetime.now(timezone.utc) + timedelta(hours=24),  # 만료 시간
    "sub": 1,            # subject - 누구의 토큰인지 (보통 user_id)
    "hello": "world"     # 아무 정보나 추가 가능
}

# 토큰 생성 (인코딩)
access_token = jwt.encode(payload, "secret", algorithm="HS256")
print("토큰:", access_token)

# 토큰 검증 (디코딩)
decoded = jwt.decode(access_token, "secret", algorithms=["HS256"])
print("디코딩 결과:", decoded)