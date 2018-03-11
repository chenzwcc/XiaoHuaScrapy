# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.http.request import Request
from XiaoHua.items import HuyaItem

class HuyaSpider(scrapy.Spider):
    name = 'huya'
    allowed_domains = ['www.huya.com']
    start_urls = ['http://www.huya.com/g/wzry']


    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        items_list = hxs.select('//div[@class="box-bd"]/ul[@class="live-list clearfix"]/li')
        # print(items)
        for i in items_list:
            item = HuyaItem()
            item['user_imge'] = i.select('.//span[@class="avatar fl"]/img/@data-original').extract_first()
            item['user_title'] = i.select('.//a[@class="title new-clickstat"]/text()').extract_first()
            item['user_name'] = i.select('.//span[@class="avatar fl"]/i[@class="nick"]/text()').extract_first()
            item['user_url'] = i.select('.//a[@class="video-info new-clickstat "]/@href').extract_first()
            item['user_attention'] = i.select('.//span[@class="num"]/i[@class="js-num"]/text()').extract_first()

            yield item

        # page_urls = hxs.select('//')


