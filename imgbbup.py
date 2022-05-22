# from imgbb.client import Client
# import os
# import aiohttp
# import asyncio
# key = os.getenv('d889e8da87c9070b622a1dc576797216')
# session = aiohttp.ClientSession()
# myclient = Client(key,session)

# async def upload(image,name):
#     response = await myclient.post(image,name)
#     url = response['data']['url']
#     print(f'Uploaded image URL: {url}')

# if __name__=='__main__':
#     asyncio.run(upload('3.jpeg','hellofile'))

import base64
import requests

req_file = '3.jpeg'

with open(req_file, "rb") as file:
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": 'd889e8da87c9070b622a1dc576797216',
        "image": base64.b64encode(file.read()),
    }
    res = requests.post(url, payload)
    filename = res.json()['data']['url']
    print(filename)
