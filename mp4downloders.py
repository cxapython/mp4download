# -*- coding: utf-8 -*-
# @Time : 2019/2/13 8:17 PM
# @Author : cxa
# @File : mp4downloders.py
# @Software: PyCharm
import requests
from tqdm import tqdm
import os
import aiohttp
import asyncio

try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except ImportError:
    pass


async def fetch(session, url, dst, pbar=None, headers=None):
    if headers:
        async with session.get(url, headers=headers) as req:
            with(open(dst, 'ab')) as f:
                while True:
                    chunk = await req.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    pbar.update(1024)
            pbar.close()
    else:
        async with session.get(url) as req:
            return req


async def async_download_from_url(url, dst):
    '''异步'''
    async with aiohttp.ClientSession() as session:
        req = await fetch(session, url, dst)

        file_size = int(req.headers['content-length'])
        print(f"获取视频总长度:{file_size}")
        if os.path.exists(dst):
            first_byte = os.path.getsize(dst)
        else:
            first_byte = 0
        if first_byte >= file_size:
            return file_size
        header = {"Range": f"bytes={first_byte}-{file_size}"}
        pbar = tqdm(
            total=file_size, initial=first_byte,
            unit='B', unit_scale=True, desc=dst)
        await fetch(session, url, dst, pbar=pbar, headers=header)


def download_from_url(url, dst):
    '''同步'''
    response = requests.get(url, stream=True)
    file_size = int(response.headers['content-length'])
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": f"bytes={first_byte}-{file_size}"}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=dst)
    req = requests.get(url, headers=header, timeout=60, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


if __name__ == '__main__':
    # 异步方式下载
    url = "http://v11-tt.ixigua.com/7da2b219bc734de0f0d04706a9629b61/5c77ed4b/video/m/220d4f4e99b7bfd49efb110892d892bea9011612eb3100006b7bebf69d81/?rc=am12NDw4dGlqajMzNzYzM0ApQHRAbzU6Ojw8MzQzMzU4NTUzNDVvQGgzdSlAZjN1KWRzcmd5a3VyZ3lybHh3Zjc2QHFubHBfZDJrbV8tLTYxL3NzLW8jbyMxLTEtLzEtLjMvLTUvNi06I28jOmEtcSM6YHZpXGJmK2BeYmYrXnFsOiMzLl4%3D"
    task = [asyncio.ensure_future(async_download_from_url(url, f"{i}.mp4")) for i in range(1, 12)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(task))
    loop.close()
    # 注释部分是同步方式下载。
    # url = "http://v11-tt.ixigua.com/7da2b219bc734de0f0d04706a9629b61/5c77ed4b/video/m/220d4f4e99b7bfd49efb110892d892bea9011612eb3100006b7bebf69d81/?rc=am12NDw4dGlqajMzNzYzM0ApQHRAbzU6Ojw8MzQzMzU4NTUzNDVvQGgzdSlAZjN1KWRzcmd5a3VyZ3lybHh3Zjc2QHFubHBfZDJrbV8tLTYxL3NzLW8jbyMxLTEtLzEtLjMvLTUvNi06I28jOmEtcSM6YHZpXGJmK2BeYmYrXnFsOiMzLl4%3D"
    #
    # download_from_url(url, "夏目友人帐第一集.mp4")
