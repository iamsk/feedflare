from time import mktime
from datetime import datetime, timedelta
import requests
import feedparser
from benedict import benedict


def _shorten(text, width):
    if len(text) > width:
        return text[:width - 3] + '...'
    else:
        return text


class RSS(object):
    def __init__(self, rss_url):
        self.rss_url = rss_url

    def get(self):
        try:
            resp = requests.get(self.rss_url, timeout=10, verify=False)
            ret = feedparser.parse(resp.text)
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
