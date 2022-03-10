import feedparser
from datetime import datetime, timedelta
from benedict import benedict
from vika import Vika

from feishu import Feishu
from config import VIKA_TOKEN, VIKA_CONFIG_TABLE

vika = Vika(VIKA_TOKEN)


def get_feeds(vika_table):
    datasheet = vika.datasheet(vika_table, field_key="name")
    rss_list = datasheet.records.all()
    all_feeds = []
    for rss in rss_list:
        if not all([rss.标题, rss.RSS源]):
            continue
        feeds = get_feed(rss.RSS源)
        all_feeds.extend(feeds)
    # needs order by published_parsed desc
    return all_feeds


def get_feed(rss_url):
    ret = feedparser.parse(rss_url)
    records = []
    for entry in ret.entries[:3]:
        # TODO
        # print(entry.published_parsed > datetime.today() - timedelta(days=1))
        keys = ['title', 'link', 'published', 'summary', 'author', 'published_parsed', 'tags']
        record = benedict(entry).subset(keys=keys)
        record['tags'] = [tag['term'] for tag in entry.tags]
        records.append(record)
    return records


def run():
    datasheet = vika.datasheet(VIKA_CONFIG_TABLE, field_key="name")
    configs = datasheet.records.all()
    for config in configs:
        if not all([config.标题, config.feishu_webhook, config.vika_table]):
            continue
        articles = get_feeds(config.vika_table)
        fs = Feishu(config.feishu_webhook, articles)
        fs.run()


if __name__ == '__main__':
    run()
