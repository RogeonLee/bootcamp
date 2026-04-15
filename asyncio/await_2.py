import asyncio

# 1) await는 반드시 비동기 함수 안에서만 사용할 수 있습니다.
# def hello(): X
# await asyncio.sleep(3)

# 2) await 할 수 있는 코드 앞에만 await 를 쓸 수 있다.
async def hi():
    print("start hello..")
    await asyncio.sleep(2)
    print("end hello..")

async def main():
    print("start main..")
    coro = hi()
    await coro
    print("end main..")

asyncio.run(main())
