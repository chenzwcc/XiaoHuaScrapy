# -*- coding:utf:8 -*-

from twisted.internet import reactor
from twisted.web.client import getPage
from twisted.internet import defer


def response(content):
    print(content)


@defer.inlineCallbacks
def task():
    url = 'http://www.baidu.com'
    d = getPage(url.encode('utf-8'))
    d.addCallback(response)
    yield d


def down(*args,**kwargs):
    reactor.stop()

d = task()
dd = defer.DeferredList([d,])
dd.addBoth(down)

reactor.run()


