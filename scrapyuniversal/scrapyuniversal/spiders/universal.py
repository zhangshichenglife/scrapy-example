# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.configs.utils import get_config
from scrapyuniversal.configs.rules import rules
from scrapyuniversal.items import *


class UniversalSpider(CrawlSpider):

    name = 'universal'
    def __init__(self, name, *args, **kwargs):
        universal_config = get_config(name)
        self.universal_config = universal_config
        self.rules = rules.get(universal_config.get('rules'))
        self.start_urls = universal_config.get('start_urls')
        self.allowed_domains = universal_config.get('allowed_domains')
        self.item_config = get_config('item')
        super(UniversalSpider, self).__init__(*args, **kwargs)


    def parse_item(self, response):
        item = self.item_config.get('item')
        if item:
            cls = eval(item.get('class'))()
            loader = eval(item.get('loader'))(item=cls, response=response)

            for key, value in item.get('attrs').items():
                for extractor in value:
                    if extractor.get('method') == 'xpath':
                        loader.add_xpath(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'value':
                        loader.add_value(key, *extractor.get('args'), **{'re': extractor.get('re')})
                    if extractor.get('method') == 'attr':
                        loader.add_value(key, getattr(response, *extractor.get('args')))
            item = loader.load_item()
            yield item


