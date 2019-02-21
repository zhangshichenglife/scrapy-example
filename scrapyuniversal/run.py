import sys
from scrapy.utils.project import get_project_settings
from scrapyuniversal.configs.utils import get_config
from scrapy.crawler import CrawlerProcess
from scrapyuniversal.spiders.universal import UniversalSpider

def run():
    name = 'universal'

    custom_settings = get_config(name)
    print(custom_settings)
    # 爬取使用的Spider名称
    spider = custom_settings.get('spider')
    print(spider)
    project_settings = get_project_settings()
    print(dict(project_settings))
    settings = dict(project_settings.copy())
    # 合并配置
    settings.update(custom_settings.get('settings'))
    print(settings)
    process = CrawlerProcess(settings)
    # 启动爬虫
    process.crawl(spider, **{'name': name})
    process.start()


if __name__ == '__main__':
    run()