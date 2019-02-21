# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from images360.items import Images360Item
from scrapy import Spider, Request
from urllib.parse import urlencode
import json


class ImagesSpider(CrawlSpider):
    name = 'images'
    allowed_domains = ['images.so.com']
    #start_urls = ['']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    def start_requests(self):
        data = {
            'ch': 'photography',
            'listtype': 'new',
            'temp': '1'
        }

        base_url = 'https://image.so.com/zj?'
        for page in range(self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        item = Images360Item()
        result = json.loads(response.text)
        print('====================================================')
        #print(result.get('list'))
        for image in result.get('list'):
            item['id'] = image.get('imageid')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('group_title')
            item['thumb'] = image.get('qhimg_thumb_url')
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()

            yield item
