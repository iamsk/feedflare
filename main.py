import argparse
from time import mktime
from datetime import datetime, timedelta
import feedparser
from vika import Vika
from benedict import benedict

from feishu import Feishu
from config import VIKA_TOKEN, VIKA_TABLE, FEISHU_BOT_WEBHOOK

vika = Vika(VIKA_TOKEN)


def _shorten(text, width):
    if len(text) > width:
        return text[:width - 3] + '...'
    else:
        return text


def get_feeds(vika_table):
    datasheet = vika.datasheet(vika_table, field_key="name")
    rss_list = datasheet.records.all()
    all_feeds = []
    for rss in rss_list:
        if not all([rss.标题, rss.RSS源]):
            continue
        print(rss.标题)
        feeds = get_feed(rss.RSS源)
        all_feeds.extend(feeds)
    # todo order by published desc
    return all_feeds


def get_feed(rss_url):
    try:
        ret = feedparser.parse(rss_url)
    except Exception as e:
        return []
    records = []
    for entry in ret.entries[:3]:  # limit to new articles within yesterday
        try:
            dt = datetime.fromtimestamp(mktime(entry.published_parsed))
        except Exception as e:
            # some feeds missed published_parsed, example, https://www.insightpartners.com/blog/rss/
            continue
        if dt < (datetime.utcnow() - timedelta(days=1, minutes=3)):
            continue
        keys = ['title', 'link', 'published', 'summary', 'author', 'published_parsed', 'tags']
        record = benedict(entry).subset(keys=keys)
        record['summary'] = _shorten(record['summary'], 200)
        # record['tags'] = [tag['term'] for tag in entry.tags]
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
        print(config.标题)
        articles = get_feeds(config.vika_table)
        source = '<a href="https://vika.cn/workbench/{}">{}</a>'.format(config.vika_table, config.标题)
        fs = Feishu(config.feishu_webhook, articles, source)
        fs.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--type', default='individual', choices=['individual', 'team'])
    args = parser.parse_args()
    if args.type == 'team':
        run_team()
    else:
        run_individual()
