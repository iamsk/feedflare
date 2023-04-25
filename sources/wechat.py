import requests
from datetime import datetime

from config import WECHAT_COOKIE, N_TOKEN


class NewRank(object):
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'DNT': '1',
        'Origin': 'https://newrank.cn',
        'Pragma': 'no-cache',
        'Referer': 'https://newrank.cn/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'n-token': N_TOKEN,
        'sec-ch-ua': '"Not:A-Brand";v="99", "Chromium";v="112"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
    }

    def __init__(self, account):
        self.account = account

    def get(self):
        data = {
            'account': self.account,
        }
        response = requests.post('https://gw.newrank.cn/api/wechat/xdnphb/detail/v1/rank/article/lists',
                                 headers=self.headers, data=data, cookies=WECHAT_COOKIE)
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
    NewRank('zhanhao668').get()
