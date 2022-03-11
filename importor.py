import opml
import time
from vika import Vika

from config import VIKA_TOKEN, VIKA_TABLE

vika = Vika(VIKA_TOKEN)
datasheet = vika.datasheet(VIKA_TABLE, field_key="name")

outline = opml.parse('feedly.opml')

for l1 in outline:
    if l1.title in ['投资机构', '投资人blog']:
        for l2 in l1:
            print(l2.title, l2.xmlUrl)
            data = {'标题': l2.title, 'RSS源': l2.xmlUrl}
            datasheet.records.create(data)
            time.sleep(0.5)
