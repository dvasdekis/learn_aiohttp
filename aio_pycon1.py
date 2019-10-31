import time
import asyncio


async def long_running_task(time_to_sleep: int) -> None:
    print(f"Being sleep for {time_to_sleep}")
    asyncio.sleep(time_to_sleep)
    print(f"awake {time_to_sleep}")


async def run_task():
    await long_running_task(2)


asyncio.run(run_task())
"""
asyncio.run(long_running_task(2))
asyncio.run(long_running_task(3))
"""