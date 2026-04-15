import time
import asyncio

async def a():
    print("A 작업 시작")    # a() 실행 시작
    await asyncio.sleep(5)  # 2s 대기 -> 양보
    print("A 작업 종료")    # a() 실행 종료

async def b():
    print("B 작업 시작")    # b() 실행 시작
    await asyncio.sleep(2)  # 2s 대기 -> 양보
    print("B 작업 종료")    # b() 실행 종료

async def main():
    coro1 = a()
    coro2 = b()
    await asyncio.gather(coro1, coro2)  # 동시에 실행

start = time.time()
asyncio.run(main())
end = time.time()

print(f"총 소요 시간: {end - start:.2f}초")