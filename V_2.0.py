'''
V_2.0
此版本为并行下载呆站（https://www.derpibooru.org/images）图片
'''

import asyncio, aiohttp, aiofile
import re
import requests
import os
import time

# 反爬
headers = {
    'User-Agent': 'Starlight Glimmer'
}

def get_img_http(url, error_threshold = 0):
    '''
    获取图片的网址
    '''
    if error_threshold < 3:
        error_threshold += 1
        try:
            # 请求网页信息
            response = requests.get(url, headers=headers)
            html = response.text

            # 解析网页
            # 正则匹配图片网址
            urls = re.findall('<a href="(.*?)" rel="(.*?)" title="(.*?)">', html)
            img_url = urls[2][0]
            return img_url
        except:
            get_img_http(url, error_threshold)

async def img_download(session, url, save_file_name):
    '''
    download image
    '''
    img_name = url.split("/")[-1]
    print('start save img: {}'.format(img_name))
    async with session.get(url, verify_ssl=False) as resp:
        resp = await resp.content.read()
        async with aiofile.async_open(os.path.join(save_file_name, img_name), "wb") as f:
            await f.write(resp)
    print('accomplish save img: {}'.format(img_name))

async def main(urls, save_file_name):
    '''
    并行任务
    '''
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.create_task(img_download(session, url, save_file_name)) for url in urls]
        await asyncio.wait(tasks)

if __name__ == '__main__':
    # 呆站网址
    url_http = 'https://www.derpibooru.org/images/'
    # 图片保存路径
    save_file_name = 'E:/JustRelax/MyLittlePony/pony_image_from_derpibooru/1_10000'     # 此处修改为你的存储路径
    # 图片保存的起始位与结束位(实际效果为 10*start 至 10*end)
    st_en = {'star': 68, 'end': 100}
    # 存储图片链接
    urls = []

    for url_num_0 in range(st_en['star'], st_en['end']):
        time.sleep(4)
        sta = time.time()
        for url_num_1 in range(10*url_num_0, 10*(url_num_0+1)):
            time.sleep(1)
            urls.append(get_img_http(os.path.join(url_http, str(url_num_1))))
        asyncio.run(main(urls, save_file_name))
        urls.clear()
        print('本轮次用时：{}'.format(time.time() - sta))

    print('!!!!congratution!!!!')