# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class BjepbItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    wenshu = Field()
    bcfdw = Field()
    wf_type = Field()
    time = Field()
    text_url = Field()
    zxqk = Field()