# -*- coding: utf-8 -*
import argparse
import time

from vika import Vika

from targets.feishu import Feishu
from config import VIKA_TOKEN, VIKA_TABLE, FEISHU_BOT_WEBHOOK
from sources.rss import RSS
from sources.wechat import NewRank

vika = Vika(VIKA_TOKEN)


def get_feeds(vika_table):
    datasheet = vika.datasheet(vika_table, field_key="name")
    source_list = datasheet.records.all()
    all_feeds = []
    for source in source_list:
        print(source.RSS源)
        if not all([source.标题, source.RSS源]):
            continue
        if source.类型 == 'WECHAT':
            feeds = NewRank(source.RSS源).get()
            time.sleep(3)
        else:
            feeds = RSS(source.RSS源).get()
        all_feeds.extend(feeds)
    # todo order by published desc
    return all_feeds


def run_individual():
    articles = get_feeds(VIKA_TABLE)
    source = '<a href="https://vika.cn/workbench/{}">{}</a>'.format(VIKA_TABLE, '信息源')
    fs = Feishu(FEISHU_BOT_WEBHOOK, articles, source)
    fs.run()


def run_team():
    datasheet = vika.datasheet(VIKA_TABLE, field_key="name")
    configs = datasheet.records.all()
    for config in configs:
        if not all([config.标题, config.feishu_webhook, config.vika_table]):
            continue
        print(config.标题)
        articles = get_feeds(config.vika_table)
        if not articles:
            continue
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
