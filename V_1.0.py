'''
V_1.0
此版本为串行下载呆站（https://www.derpibooru.org/images）图片
'''

import time
import requests
import re
import os


# 更改请求（反爬）
headers = {
    'User-Agent': 'Starlight Glimmer'
}

def img_download(save_file_name, url, error_threshold = 0):
    '''
    图片爬取
    '''

    if error_threshold <= 3:
        error_threshold += 1
        try:
            # 请求网页，获取网页信息
            response = requests.get(url, headers=headers)
            html = response.text

            # 解析网页
            # 正则匹配图片网址
            urls = re.findall('<a href="(.*?)" rel="(.*?)" title="(.*?)">', html)
            img_http = urls[2][0]

            # 保存图片
            # 图片命名
            img_name = img_http.split('/')[-1]
            response_img = requests.get(img_http, headers=headers)
            with open(os.path.join(save_file_name, img_name), 'wb') as f:
                f.write(response_img.content)
        except:
            img_download(save_file_name, url, error_threshold)
        return True

if __name__ == '__main__':
    # 呆站网址
    url_http = 'https://www.derpibooru.org/images/'
    # 图片保存路径
    save_file_name = 'your file name'
    # 图片保存的起始位与结束位
    st_en = {'star': 101, 'end': 200}

    for url_num in range(st_en['star'], st_en['end']+1):
        # 等待5秒钟，防止网站崩溃
        time.sleep(5)
        url = os.path.join(url_http, str(url_num))
        tag = img_download(save_file_name, url)
        if tag:
            print('successfully save image: {}'.format(url_num))
