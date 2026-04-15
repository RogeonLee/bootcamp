import time

# 중복 계산 없이 팩토리얼을 계산하는 제너레이터 함수
def factorial(n): # 팩토리얼 계산을 제너레이터로 구현
    ans = 1     # 초기값 설정
    for i in range(1, n+1): # 1부터 n까지 반복하면서 팩토리얼 계산
        ans *= i # ans에 i를 곱해서 팩토리얼 계산
        yield ans # 계산된 팩토리얼 값을 yield로 반환, 다음 호출 시 이어서 계산

start = time.time() # 시작 시간 기록

gen = factorial(1000) # 팩토리얼 제너레이터 객체 생성, 1000까지의 팩토리얼 계산 준비

# 1000번 next() 호출하여 팩토리얼 계산 진행, 마지막 결과는 1000!이 됨
result = None 
for _ in range(1000):
    result = next(gen)
print(f"결과: {result}")
# 팩토리얼 계산이 끝난 후 결과 출력, 1000!의 값이 출력됨

# 팩토리얼 계산이 끝난 후 종료 시간 기록 및 실행 시간 출력
end = time.time()
print(f"실행 시간: {(end - start)*1000}ms")
# 팩토리얼 계산이 끝난 후 실행 시간 출력, ms 단위로 변환하여 표시