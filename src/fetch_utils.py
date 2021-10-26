import aiohttp


async def async_post_request(_url: str, json_data: dict, headers: dict) -> tuple:
    """
    **async_post_request**
        asynchronous post request
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=_url, json=json_data, headers=headers) as response:
                json_data: dict = await response.json()
                return json_data, response.status
        except aiohttp.ClientConnectorError:
            return None, 406


async def async_get_request(_url: str, headers: dict) -> tuple:
    """
        **async_get_request**
            asynchronous get request
    :param _url:
    :param headers:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url=_url, headers=headers) as response:
                json_data: dict = await response.json()
                return json_data, response.status
        except aiohttp.ClientConnectorError:
            return None, 406  # remote data error
