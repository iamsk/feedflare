import argparse
from time import mktime
from datetime import datetime, timedelta
import feedparser
from vika import Vika
from benedict import benedict

from feishu import Feishu
from config import VIKA_TOKEN, VIKA_TABLE, FEISHU_BOT_WEBHOOK

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
    # todo order by published desc
    return all_feeds


def get_feed(rss_url):
    ret = feedparser.parse(rss_url)
    records = []
    for entry in ret.entries[:3]:  # limit to new articles within yesterday
        dt = datetime.fromtimestamp(mktime(entry.published_parsed))
        if dt < (datetime.utcnow() - timedelta(days=1)):
            continue
        keys = ['title', 'link', 'published', 'summary', 'author', 'published_parsed', 'tags']
        record = benedict(entry).subset(keys=keys)
        record['tags'] = [tag['term'] for tag in entry.tags]
        records.append(record)
    return records


def run_individual():
    articles = get_feeds(VIKA_TABLE)
    fs = Feishu(FEISHU_BOT_WEBHOOK, articles)
    fs.run()


def run_team():
    datasheet = vika.datasheet(VIKA_TABLE, field_key="name")
    configs = datasheet.records.all()
    for config in configs:
        if not all([config.标题, config.feishu_webhook, config.vika_table]):
            continue
        articles = get_feeds(config.vika_table)
        fs = Feishu(config.feishu_webhook, articles)
        fs.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', default='individual', choices=['individual', 'team'])
    args = parser.parse_args()
    if args.type == 'team':
        run_team()
    else:
        run_individual()
