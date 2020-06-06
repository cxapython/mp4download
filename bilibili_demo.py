# -*- coding: utf-8 -*-
from __future__ import print_function
import requests
from tqdm import tqdm
from .ffmpeg import ffmpeg_concat_av

base_url = "https://www.bilibili.com/video/av455536018"
headers = {"Referer": base_url,
           "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36"}
mp4_url = "http://upos-sz-mirrorks3c.bilivideo.com/upgcxcode/91/02/188640291/188640291-1-30080.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1591428111&gen=playurl&os=ks3cbv&oi=1875198200&trid=e522a29e4fc14b0380f3ad6f8b82cb1du&platform=pc&upsig=c40c48526c89866aee04d1e1ccc59acd&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&orderid=1,2&logo=40000000"
mp3_url = "http://upos-sz-mirrorks3c.bilivideo.com/upgcxcode/91/02/188640291/188640291-1-30280.m4s?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1&deadline=1591428111&gen=playurl&os=ks3cbv&oi=1875198200&trid=e522a29e4fc14b0380f3ad6f8b82cb1du&platform=pc&upsig=4a62977e3936823d4484c6e96bebfa58&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&orderid=1,2&logo=40000000"

chunk = 1024 * 256


def download(file_name, url, first_byte=0):
    r = requests.get(url, headers=headers, stream=True)
    file_size = int(r.headers["content-length"])
    print(file_size)
    pbar = tqdm(
        total=file_size + first_byte, initial=first_byte,
        unit='B', unit_scale=True, desc=file_name)
    with open(file_name, "ab+") as fs:
        for buff in r.iter_content(chunk_size=chunk):
            fs.write(buff)
            fs.flush()
            pbar.update(chunk)
    pbar.close()


if __name__ == '__main__':
    first_byte = 33030144
    headers["range"] = "bytes={}-".format(first_byte)
    download("1_new.m4s", mp4_url, first_byte)
    if first_byte != 0:
        headers["range"] = "bytes=0-"
        download("2_new.m4s", mp3_url)
        ffmpeg_concat_av(["1_new.m4s", "2_new.m4s"], "3_new.mp4")
