import asyncio
import aiohttp
import time

urlset = ["https://www.python.org/dev/peps/pep-8010/", "https://www.python.org/dev/peps/pep-8011/",
          "https://www.google.co.za"]


async def fetch_url(myurl):
    async with aiohttp.ClientSession() as session:
        async with session.get(myurl) as resp:
            content = await resp.read()
            print(content[-1:])
            return content


async def main() -> None:
    tasks = []
    for each_url in urlset:
        tasks.append(fetch_url(each_url))
    await asyncio.wait(tasks)

if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - start
    print(f"This took {elapsed}")