# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from XiaoHua.items import TencentItem


class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['https://hr.tencent.com/position.php']

    has_request_set = {}

    def parse(self, response):
        # print(response)
        htx = HtmlXPathSelector(response)

        info_list = htx.select('//tr[@class="even"]|//tr[@class="odd"]')
        for info in info_list:
            item = TencentItem()
            item['position_name'] = info.xpath('.//td[@class="l square"]/a/text()').extract_first()
            item['position_type'] = info.xpath('.//td/text()').extract()[0]
            item['position_people'] = info.xpath('.//td/text()').extract()[1]
            item['position_location'] = info.xpath('.//td/text()').extract()[2]
            item['position_release_time'] = info.xpath('.//td/text()').extract()[3]

            yield item

        # page_urls = htx.select('//div[@class="pagenav"]/a[re:test(@href,"position.php?&start=\d+#a")]/@href').extract()
        page_urls = htx.select('//div[@class="pagenav"]/a/@href').extract()
        page_urls = set(page_urls)
        page_urls = list(page_urls)
        for url in page_urls:
            if url.endswith('javascript:;'):
                page_urls.remove(url)
        for url in page_urls:
            key = self.md5(url)
            if key in self.has_request_set:
                pass
            else:
                self.has_request_set[key] = url
                url = 'https://hr.tencent.com/' + url
                yield Request(url, callback=self.parse)

    @staticmethod
    def md5(val):
        import hashlib
        ha = hashlib.md5()
        ha.update(bytes(val, encoding='utf-8'))
        key = ha.hexdigest()
        return key
