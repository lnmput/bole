# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
from scrapy.loader  import ItemLoader

def addTitleLast(title):
    return title + '-bole'


def addTitleFirst(title):
    return 'yangzie' + title

def defaultValue(value):
    return value

class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 系统自动生成的
    pass

class CustomItemLoader(ItemLoader):
    # 自定义itemloader, 取第一个
    default_output_processor = TakeFirst()


class ArticleItem(scrapy.Item):
    # 我们自己定义的,使用这个
    title = scrapy.Field(
        # 可以传入多个预处理函数
        input_processor = MapCompose(addTitleFirst, addTitleLast)
    )
    url = scrapy.Field()
    url_id = scrapy.Field()
    image = scrapy.Field(
        # 仅仅覆盖默认, 不做任何处理
        output_processor=MapCompose(defaultValue)
    )
    image_path = scrapy.Field()