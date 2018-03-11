# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import requests
import json
import codecs


class XiaohuaPipeline(object):
    def process_item(self, item, spider):
        return item


class FilePipeline(object):
    def __init__(self):
        if not os.path.exists('imgs'):
            os.mkdir('imgs')

    def process_item(self, item, spider):
        response = requests.get(url=item['img'], stream=True)
        file_name = '%s.jpg' % item['name']
        with open(os.path.join('imgs', file_name), 'wb') as f:
            f.write(response.content)
        return item


class JsonPipeline(object):

    def __init__(self):
        self.file = codecs.open('huya.json', 'w', encoding='utf-8')

    def process_item(self,item,spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def close_spider(self,spider):
        self.file.close()


class TencentJsonPipeline(object):

    def __init__(self):
        self.file = codecs.open('tencent.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def close_spider(self, spider):
        self.file.close()


class DoubanJsonPipleline(object):

    def __init__(self):
        self.file = open('douban.json', 'wb')

    def process_item(self,item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(lines.encode('utf-8'))
        return item

    def close_spider(self,spider):
        self.file.close()