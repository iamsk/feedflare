import requests
import json
import time
from datetime import date


class Feishu(object):
    def __init__(self, webhook, records):
        self.webhook = webhook
        self.records = records
        if not records:
            exit(0)

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
                    "content": "**{}**\n\n[“{}”]({}) - {}".format(record['summary'], record['title'], record['link'],
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
                    "content": "💡本次内容分享自 xx，你想在这里看到什么样的内容？给我们留言吧",
                    "tag": "plain_text"
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
    fs = Feishu(WEBHOOK_URL, [])
    fs.run()
