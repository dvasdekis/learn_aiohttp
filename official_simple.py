import asyncio
import random
# Simple pub/sub in official docs: https://asyncio.readthedocs.io/en/latest/producer_consumer.html


async def produce(queue, n):
    for x in range (0, n):
        print('producing {}/{}'.format(x, n))  # produce an item
        await asyncio.sleep(random.random())  # Simulate I/O
        item = str(x)
        await queue.put(item)

    await queue.put(None)  # Indicate that the producer is done via sending 'None' in the queue


async def consume(queue):
    while True:
        item = await queue.get()  # Wait for an item from the producer
        if item is None:
            break  # Use None signal to indicate a finished queue

        print('consuming item {}'.format(item))  # process the item
        await asyncio.sleep(random.random())  # simulate I/O


async def main():
    # A queue must be created within a loop. asyncio.run() creates our loop for us, so we can avoid the binding of
    # the queue to the loop if we create the queue within the context of the loop
    queue = asyncio.Queue()
    await asyncio.gather(produce(queue, 10), consume(queue))


if __name__ == '__main__':
    asyncio.run(main())
