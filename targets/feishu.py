import requests
import json
import time
from datetime import date


class Feishu(object):
    def __init__(self, webhook, records, source):
        self.webhook = webhook
        self.records = records
        self.source = source

    @staticmethod
    def gen_data(articles):
        data = {
            "config": {
                "wide_screen_mode": True
            },
            "header": {
                "template": "blue",
                "title": {
                    "content": "🎉 {} #今日动态#".format(date.today()),
                    "tag": "plain_text"
                }
            },
            "elements": articles
        }
        return {"msg_type": "interactive", 'card': json.dumps(data)}

    def run(self):
        articles = []
        for record in self.records:
            article = {
                "tag": "div",
                "text": {
                    "content": "**{}**\n[“{}”]({}) - {}".format(record['summary'], record['title'], record['link'],
                                                                record['author']),
                    "tag": "lark_md"
                }
            }
            articles.append(article)
            articles.append({
                "tag": "hr"
            })
            # import pdb;pdb.set_trace()
            time.sleep(0.3)
        articles.append({
            "elements": [
                {
                    "content": "💡 扩展内容请更新 {}！".format(self.source),
                    "tag": "lark_md"
                }
            ],
            "tag": "note"
        })
        data = self.gen_data(articles)
        r = requests.post(self.webhook, json=data).json()
        print(r)


if __name__ == '__main__':
    # testing
    WEBHOOK_URL = 'https://open.feishu.cn/open-apis/bot/v2/hook/bd78c3f3-ac60-4ba3-b850-19e31f0e9b40'
    fs = Feishu(WEBHOOK_URL, [], '')
    fs.run()
