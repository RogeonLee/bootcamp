import asyncio
import time


async def request1():
    print("[1] 새로운 웹 요청...")
    await asyncio.sleep(2)
    print("[1] 응답...")


async def request2():
    print("[2] 새로운 웹 요청...")
    await asyncio.sleep(5)
    print("[2] 응답...")


async def main():
    coro1 = request1()
    coro2 = request2()
    await asyncio.gather(coro1, coro2)


start = time.time()
asyncio.run(main())
end = time.time()

print(f"총 소요시간: {end - start:.2f}초")
# 비동기 실행 → 약 5초 (max(2, 5))
# 동기였다면 7초 (2 + 5)
