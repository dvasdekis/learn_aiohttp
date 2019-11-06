import asyncio
import logging
import random
import string
import uuid
import time
# from https://www.youtube.com/watch?v=bckD_GK80oY
logging.basicConfig(level="INFO")
LOG = logging.getLogger('')

""" 
Learnings:
- Queues will increase in size rapidly if your producer is faster than your consumer. 
    Use a Max queue size parameter when you instantiate your queue to deal with this nicely. (Queue.put() is aware) 
"""


async def publish(queue):
    while True:
        choices = string.ascii_lowercase + string.digits
        host_id = "".join(random.choices(choices, k=4))
        msg = f"""Message(
            msg_id={str(uuid.uuid4())},
            inst_name="cattle-{host_id}"
        )"""
        LOG.info("Started publishing")
        await asyncio.create_task(queue.put(msg))  # Schedules the coroutine on the loop without blocking
        LOG.info(f"Published {msg}")


async def handle_message(msg):
    async def restart_host(msg):
        # simulating IO work
        await asyncio.sleep(random.random())
        LOG.info(f"Restarted {msg}")

    async def save(msg):
        # simulating IO work
        await asyncio.sleep(random.random())
        LOG.info(f"Saved {msg} into dattabase")

    async def cleanup(msg):
        await asyncio.sleep(random.random())
        LOG.info(f"Done. Acked {msg}")

    await asyncio.gather(save(msg), restart_host(msg))
    await cleanup(msg)


async def consume(queue):
    while True:
        msg = await queue.get()
        LOG.info(f"Consumed {msg}")
        await asyncio.create_task(handle_message(msg))  # Simulates a random IO operation


async def main() -> None:
    queue = asyncio.Queue(maxsize=10)
    LOG.info("Created queue")
    try:
        await asyncio.gather(publish(queue), consume(queue))
    except KeyboardInterrupt:
        LOG.info("Process interrupted")
    finally:
        logging.info("Cleaning up")


if __name__ == "__main__":
    LOG.info("Started main loop")
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"This took {elapsed}")
    LOG.info("Finished main loop")