import string
import random
import hashlib
import requests
from datetime import datetime, timedelta

from config import WECHAT_COOKIE


class NewRank(object):
    headers = {
        'authority': 'newrank.cn',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/x-www-form-urlencoded',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://newrank.cn',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://newrank.cn/new/readDetial?account=SouthReviews',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': WECHAT_COOKIE,
    }
    path = '/xdnphb/detail/v1/rank/article/lists'

    def __init__(self, account):
        self.account = account
        self.nonce = self.get_nonce()
        self.xyz = self.get_xyz()
        self.headers['referer'] = 'https://newrank.cn/new/readDetial?account={}'.format(account)

    @staticmethod
    def get_nonce():
        num_str = string.digits + string.ascii_lowercase[:6]
        return ''.join(random.sample(num_str, 9))

    def get_xyz(self):
        # 9位随机数
        # 获取xyz的输入值
        h = f'{self.path}?AppKey=joker&account={self.account}&nonce={self.nonce}'
        # md5加密获取xyz
        xyz = hashlib.md5(h.encode('utf-8')).hexdigest()
        return xyz

    def get(self):
        data = {
            'account': self.account,
            'nonce': self.nonce,
            'xyz': self.xyz
        }
        response = requests.post('https://newrank.cn' + self.path, headers=self.headers, data=data)
        try:
            value = response.json()['value']
        except Exception as e:
            print(e)
            return []
        if value == -999:
            return []
        records = []
        for batch in value['realTimeArticles']:
            for article in batch:
                yesterday_str = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
                if article['publicTime'].startswith(yesterday_str):
                    continue
                data = {'title': article['title'], 'link': article['url'], 'author': self.account, 'summary': ''}
                records.append(data)
        return records


if __name__ == '__main__':
    NewRank('SouthReviews').get()
