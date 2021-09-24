from typing import Optional
import aiohttp


async def async_post_request(_url, json_data, headers) -> tuple:
    async with aiohttp.ClientSession() as session:
        async with session.post(url=_url, json=json_data, headers=headers) as response:
            json_data: dict = await response.json()
            return json_data, response.status


async def async_get_request(_url, headers) -> tuple:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=_url, headers=headers) as response:
                json_data: dict = await response.json()
                return json_data, response.status
        except aiohttp.ClientConnectorError:
            return None, 406 # remote data error
