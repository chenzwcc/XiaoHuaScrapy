# -*- coding:utf:8 -*-
__author__ = 'chenzwcc'

from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet import defer


class Request(object):
    def __init__(self, url, callback):
        self.url = url
        self.callback = callback


class ChoutiSpider(object):
    name = 'chouti'

    def start_requests(self):
        start_url = ['http://www.baidu.com', 'http://www.bing.com']
        for url in start_url:
            yield Request(url, self.parse)

    def parse(self, response):
        print(response)


import queue

Q = queue.Queue()


class Engine(object):
    def __init__(self):
        self._close = None

    def crawl(self, spider):
        start_requests = iter(spider.start_requests())
        while True:
            try:
                request = next(start_requests)
                Q.put(request)
            except StopIteration as e:
                break
        self._close = defer.Deferred()
        yield self._close


spider = ChoutiSpider()

_active = set()
engine = Engine()
d = engine.crawl(spider)
_active.add(d)

dd = defer.DeferredList(_active)
dd.addBoth(lambda a: reactor.stop())

reactor.run()
