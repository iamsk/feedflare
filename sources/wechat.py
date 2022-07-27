import requests
from datetime import datetime

from config import WECHAT_COOKIE


class NewRank(object):
    headers = {
        'authority': 'gw.newrank.cn',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'origin': 'https://newrank.cn',
        'pragma': 'no-cache',
        'referer': 'https://newrank.cn/',
        'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    }

    def __init__(self, account, cookie):
        self.account = account
        self.headers['cookie'] = cookie.split(';')[0]
        self.headers['n-token'] = cookie.split(';')[1]

    def get(self):
        data = {
            'account': self.account,
        }
        response = requests.post('https://gw.newrank.cn/api/wechat/xdnphb/detail/v1/rank/article/lists',
                                 headers=self.headers, data=data)
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
                today_str = datetime.now().strftime('%Y-%m-%d')
                if article['updateTime'].startswith(today_str):
                    data = {'title': article['title'], 'link': article['url'], 'author': self.account, 'summary': ''}
                    records.append(data)
        # print(records)
        return records


if __name__ == '__main__':
    NewRank('zhanhao668', WECHAT_COOKIE).get()
