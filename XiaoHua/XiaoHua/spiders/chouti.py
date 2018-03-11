# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.cookies import CookieJar
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector


class ChoutiSpider(scrapy.Spider):
    name = 'chouti'
    allowed_domains = ['dig.chouti.com']
    start_urls = ['http://dig.chouti.com/']

    cookie_dict = None
    has_request_set = {}

    def parse(self, response):
        cookies = CookieJar()
        cookies.extract_cookies(response, response.request)
        self.cookie_dict = cookies._cookies

        yield Request(
            url='http://dig.chouti.com/login',
            method='POST',
            headers={'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8"},
            body='phone=8618279816872&password=18279816872&oneMonth:1',
            cookies=self.cookie_dict,
            callback=self.check_login
        )

    def check_login(self, response):
        req = Request(
            url='http://dig.chouti.com/',
            method='GET',
            callback=self.show,
            cookies=self.cookie_dict,
            dont_filter=True
        )
        yield req

    def show(self, response):

        htx = HtmlXPathSelector(response=response)
        news_list = htx.select('//div[@class="content-list"]/div[@class="item"]')

        for news in news_list:
            linkid = news.xpath('.//div[@class="part2"]/@share-linkid').extract_first()

            yield Request(
                url='http://dig.chouti.com/link/vote?linksId=%s' %(linkid,),
                method='POST',
                cookies=self.cookie_dict,
                callback=self.do

            )
        page_list = htx.select('//div[@id="dig_lcpage"]//a[re:test(@href,"/all/hot/recent/\d+")]/@href').extract()
        for page in page_list:
            page_url = 'http://dig.chouti.com%s' % page
            import hashlib
            hash = hashlib.md5()
            hash.update(bytes(page_url, encoding='utf-8'))
            key = hash.hexdigest()
            if key in self.has_request_set:
                pass
            else:
                self.has_request_set[key] = page_url
                yield Request(
                    url=page_url,
                    method='GET',
                    callback=self.show
                )

    def do(self,response):
        print(response.text)