# 동기식
# 1) 함수의 정의 : def foo(): 
# 2) 함수 호출 : foo()

# 비동기식
# 1) 코루틴 함수 정의: async def  
# 2) 코루틴 객체 생성: coro = foo()
# 3) 코루틴 객체 실행: asyncio.run(coro)
# 코루틴 함수(coroutine function)와 코루틴 객체(coroutine object)를 정의하는 모듈입니다.

async def hello():
    print("Hello")

    coro1 = hello() # 코루틴 객체 생성
    coro2 = hello() # 코루틴 객체 생성

    asyncio.run(coro1) # 코루틴 객체 실행 -> Hello 출력, return None이 생략되어있음.

    async def main():
    asyncio.run(main_coro) # main_coro 실행 -> Hello 출력, return None이 생략되어있음.