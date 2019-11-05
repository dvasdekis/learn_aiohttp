import asyncio
import logging
import random
import string
import queue
import uuid
import time
# from https://www.youtube.com/watch?v=bckD_GK80oY
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)7s: %(message)s'
)
LOG = logging.getLogger('')


async def publish(queue):
    choices = string.ascii_lowercase + string.digits
    while True:
        host_id = "".join(random.choices(choices, k=4))
        msg = Message(
            msg_id=str(uuid.uuid4()),
            inst_name=f"cattle-{host_id}"
        )
        asyncio.create_task(queue.put(msg)) # Schedules the coroutine on the loop without blocking
        LOG.info(f"Published {msg}")


async def handle_message(msg):
    async def restart_host(msg):
        # simulating IO work
        await asyncio.sleep(random.random())
        msg.restarted = True
        LOG.info(f"Restarted {msg.hostname}")

    async def save(msg):
        # simulating IO work
        await asyncio.sleep(random.random())
        msg.saved = True
        LOG.info(f"Saved {msg} into dattabase")

    async def cleanup(msg):
        msg.acked = True
        LOG.info(f"Done. Acked {msg}")

    await asyncio.gather(save(msg), restart_host(msg))
    await cleanup(msg)


async def consume(queue):
    while True:
        msg = await queue.get()
        LOG.info(f"Consumed {msg}")
        asyncio.create_task(handle_message(msg))  # Simulates a random IO operation


async def main() -> None:
    q = queue.Queue()
    while True:
        asyncio.create_task(publish(q))
        asyncio.create_task(consume(q))


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"This took {elapsed}")