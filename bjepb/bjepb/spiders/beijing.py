# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bjepb.items import BjepbItem
import base64
import json


class BeijingSpider(CrawlSpider):
    name = 'beijing'
    allowed_domains = ['services.bjepb.gov.cn']
    #start_urls = ['http://services.bjepb.gov.cn/']

    # rules = (
    #     Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    # )
    def start_requests(self):
        base_url = 'http://services.bjepb.gov.cn/eportal/admin?moduleId=f0270681ba5545089012be244338c858&struts.portlet.mode=view&struts.portlet.action=/portlet/commonSearch!getDataList.action'

        for start in range(138):
            base_data = {
                "start":str(start*10),
                "end":str(start*10 + 10),
                "appId":"",
                "sourceId":"8414f103052842d6ab59f57d93ca4b61",
                "illegUnit":"",
                "LeaderApproTime_start":"",
                "LeaderApproTime_end":"",
                "sort":"LeaderApproTime desc"
            }
            print(str(base_data))
            b1 = bytes(str(base_data).replace("'",'"'),'UTF-8')
            b2 = base64.b64encode(b1)
            params = {'params': b2.decode('utf-8')}
            yield scrapy.FormRequest(url=base_url, formdata=params, callback=self.parse_item)

    def parse_item(self, response):
        item = BjepbItem()
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        result = json.loads(response.text)
        dataList = result.get('dataList')
        url0 = 'http://services.bjepb.gov.cn/eportalapply/downfile/8414F103052842D6AB59F57D93CA4B61/{}/处罚决定书.pdf'
        if dataList:
            for li in dataList:
                item['wenshu'] = li.get('CASENUM')
                item['bcfdw'] = li.get('ILLEGUNIT')
                item['wf_type'] = li.get('RULESORT')
                item['time'] = li.get('LEADERAPPROTIME').replace(' 00:00:00.0','')
                item['text_url'] = url0.format(li.get('APPID').upper())
                item['zxqk'] = li.get('RECTIFY')

                yield item
