import asyncio

import aiohttp


async def get_response(session, url):
    async with session.get(url) as resp:
        return resp


async def main():
    async with aiohttp.ClientSession(headers={"content-type": "text/html"}) as session:
        tasks = []
        tasks.append(get_response(session, 'https://www.google.com/search?q=soundcore+life+q30'))
        response = await asyncio.gather(*tasks)
        print(response)


asyncio.run(main())
