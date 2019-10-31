import signal
import sys
import asyncio
import aiohttp
import json

loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=loop)


async def get_json(jclient, url):
    """
    Starts a client session with aiohttp, and uses it to get json from a site
    :param jclient: An aiohttp client session (defined above)
    :param url: The URL to parse
    :return: The response of the URL
    """
    async with jclient.get(url) as response:
        assert response.status == 200
        return await response.read()


async def get_reddit_top(rclient, subreddit):
    """
    Reads a subreddit with a given
    :param subreddit:
    :param rclient:
    :return:
    """
    data1 = await get_json(rclient, 'https://www.reddit.com/r/' + subreddit + '/top.json?sort=top&t=day&limit=5')
    j = json.loads(data1.decode('utf-8'))
    for i in j['data']['children']:
        score = i['data']['score']
        title = i['data']['title']
        link = i['data']['url']
        print(str(score) + ': ' + title + ' (' + link + ')')

    print('DONE:', subreddit + '\n')


def signal_handler(signal, frame):
    loop.stop()
    client.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

asyncio.gather(get_reddit_top(client, 'python'),
               get_reddit_top(client, 'programming'), 
               get_reddit_top(client, 'compsci'))
loop.run_forever()