# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader.processors import TakeFirst, Join, Compose
from scrapy.loader import ItemLoader

class ScrapyuniversalItem(Item):
    # define the fields for your item here like:
    title = Field()
    url = Field()
    text = Field()
    datetime = Field()
    source = Field()
    website = Field()

class NewsLoader(ItemLoader):
    default_input_processor = TakeFirst()

class ChinaLoader(ItemLoader):
    text_out = Compose(Join(), lambda s: s.strip())
    default_input_processor = text_out
    # text = Compose(Join(), lambda s: s.strip())
    # datetime = Compose(Join(), lambda s: s.strip())
    # source = Compose(Join(), lambda s: s.strip())
    # website = Compose(Join(), lambda s: s.strip())