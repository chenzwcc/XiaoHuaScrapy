# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request


class DaxuemmSpider(scrapy.Spider):
    name = 'daxueMM'
    allowed_domains = ['www.521609.com']
    start_urls = ['http://www.521609.com/daxuexiaohua/list31.html']

    has_request_set = {}

    def parse(self, response):

        hxs = HtmlXPathSelector(response=response)
        items = hxs.select('//div[@class="index_img list_center"]/ul/li')
        for item in items:
            img = item.select('.//a/img/@src').extract_first()
            name = item.select('.//a/img/@alt').extract_first()
            from ..items import XiaohuaItem
            img = 'http://www.521609.com/' + img
            obj = XiaohuaItem(name=name, img=img)
            yield obj

        urls = hxs.select('//a[re:test(@href,"list3\d+.html")]/@href').extract()
        for url in urls:
            key = self.md5(url)
            if key in self.has_request_set:
                pass
            else:
                self.has_request_set[key] = url
                url = 'http://www.521609.com/daxuexiaohua/' + url

                req = Request(url=url, method='GET', callback=self.parse)
                yield req

    @staticmethod
    def md5(val):
        import hashlib
        ha = hashlib.md5()
        ha.update(bytes(val, encoding='utf-8'))
        key = ha.hexdigest()
        return key