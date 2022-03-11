# feedflare

feedflare - distribute feeds to IM

![Feedflare workflow](http://processon.com/chart_image/6225bcc87d9c0836f902f34c.png "Feedflare workflow")

### Setup

```shell script
python3 -m virtualenv venv  # or virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
```

### Usage

copy config.py.tpl to config.py

1. For individual use:

![rss table](rss_table.png)

create your own rss table in vika.cn, and copy the API token and table id to config.py

https://open.feishu.cn/open-apis/bot/v2/hook/xxx

create your own feishu bot, and copy the bot webhook url to config.py

```shell
python main.py
```

2. For team use:

Please read the code for more details.

```shell
python main.py -t team
```
