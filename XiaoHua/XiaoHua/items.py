# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaohuaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    img = scrapy.Field()


class HuyaItem(scrapy.Item):
    user_imge = scrapy.Field()
    user_title = scrapy.Field()
    user_name = scrapy.Field()
    user_url = scrapy.Field()
    user_attention = scrapy.Field()


class TencentItem(scrapy.Item):
    position_name = scrapy.Field()
    position_type = scrapy.Field()
    position_people = scrapy.Field()
    position_location = scrapy.Field()
    position_release_time = scrapy.Field()


class DoubanItem(scrapy.Item):

    # 导演: 刘伟强 / 麦兆辉
    movie_director = scrapy.Field()
    # 编剧:
    movie_screenwriter = scrapy.Field()
    # 主演:
    movie_actor = scrapy.Field()
    # 类型:
    movie_type = scrapy.Field()
    # # 制片国家 / 地区:
    # movie_country = scrapy.Field()
    # # 语言:
    # movie_language = scrapy.Field()
    # 上映日期:
    movie_release_date = scrapy.Field()
    # 分钟 /
    movie_time = scrapy.Field()
    # # 又名:
    # movie_nick = scrapy.Field()
    # IMDb链接:
    movie_IMDb = scrapy.Field()
    # 评分:
    movie_rating = scrapy.Field()
