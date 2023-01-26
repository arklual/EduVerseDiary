import asyncio
import time

async def f():
    await print('Hi from f')

async def g():
    await print('Hi from g')

async def main():
    await f()
    await asyncio.sleep(5)
    await g()

asyncio.run(main())