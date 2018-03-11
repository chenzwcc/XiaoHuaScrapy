# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from XiaoHua.items import DoubanItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/top250']

    def parse(self, response):
        htx = HtmlXPathSelector(response)
        page_urls = htx.xpath('//div[@class="paginator"]/a/@href').extract()
        page_urls.append('?start=0&filter=')

        for url in page_urls:
            url = 'https://movie.douban.com/top250' + url
            yield Request(url, callback=self.deal_request)

    def deal_request(self,response):
        htx = HtmlXPathSelector(response)
        movie_urls = htx.xpath('//ol[@class="grid_view"]/li//div[@class="hd"]/a/@href').extract()
        for movie_url in movie_urls:
            yield Request(movie_url,callback=self.deal_link)

    def deal_link(self,response):
        content = HtmlXPathSelector(response)
        item = DoubanItem()
        item['movie_director'] = content.xpath('//div[@id="info"]//span[@class="attrs"]/a[@rel="v:directedBy"]/text()').extract()
        item['movie_screenwriter'] = content.xpath('//div[@id="info"]/span[2]//a/text()').extract()
        item['movie_actor'] = content.xpath('//div[@id="info"]/span[3]//a/text()').extract()
        item['movie_type'] = content.xpath('//div[@id="info"]/span[@property="v:genre"]/text()').extract()
        item['movie_release_date'] = content.xpath('//div[@id="info"]/span[@property="v:initialReleaseDate"]/text()').extract()
        item['movie_time'] = content.xpath('//div[@id="info"]/span[@property="v:runtime"]/text()').extract()
        item['movie_IMDb'] = content.xpath('//div[@id="info"]/a[@target="_blank"]/@href').extract()
        item['movie_rating'] = content.xpath('//div[@id="interest_sectl"]//strong[@class="ll rating_num"]/text()').extract()

        # item['movie_country'] = content.xpath('//div[@id="info"]/span[@class="pl"][2]/text()').extract()
        # item['movie_language'] = content.xpath('//div[@id="info"]/span[3]//a/text()').extract()
        # item['movie_nick'] = content.xpath('//div[@id="info"]/span[3]//a/text()').extract()
        yield item

