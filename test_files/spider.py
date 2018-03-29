# -*- coding: utf-8 -*-
# python 3
"""
scrapy crawl pycoder -a start_url=http://www.dmu.ac.uk
or
python3 ./...
"""
import scrapy
from scrapy.crawler import CrawlerProcess
from urllib.parse import urljoin
from scrapy.linkextractor import LinkExtractor
import re
import urllib.parse
from scrapy import log, signals
from twisted.internet import reactor
from scrapy.xlib.pydispatch import dispatcher

# class SpyderItem(scrapy.Item):
#     title = scrapy.Field()
#     body = scrapy.Field()
#     date = scrapy.Field()


class Spider(scrapy.Spider):
    name = "spider"
    # TODO: into params
    allowed_domains = ['teplo-seti.ru']
    # start_urls = [
    #     'http://www.dmu.ac.uk',
    # ]
    visited_urls = []
    result_urls = set()

    # TODO: start_url to array
    def __init__(self, start_url=None, *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]

    def parse(self, response):
        print("Current url: ", response.url)

        #Обработка текста
        # print(((response.body).decode()))
        resp_body = response.body.decode()
        # print(resp_body)
        print("результат поиска")
        # print(*list(re.findall(r'[^>]*тел[^<]*', resp_body)), sep="\n")
        print("xpath")

        print(response.xpath('//p/text()').re(r'\w*котел\w*'))#.re(r'...кот...')
        # response.xpath('//a[contains(@href, "image")]/text()').re(r'Name:\s*(.*)')



        if response.url not in self.visited_urls:
            # Вытаскиваем улры со страницы
            link_extractor = LinkExtractor()
            extracted_urls = link_extractor.extract_links(response)
            extracted_urls = list(map(lambda link: link.url, extracted_urls))

            # Якоря
            extracted_urls = list(filter(lambda x: x.rfind("#") < x.rfind("/"), extracted_urls))
            extracted_urls = list(filter(lambda x: self.allowed_domains[0] in x, extracted_urls))
            # query string
            extracted_urls = list(map(lambda x: x[0:x.rfind("?")] if x.rfind("?") > x.rfind("/") else x, extracted_urls))

            # study in url!!!!!!!!!!!!!!!!!!
            # extracted_urls = list(filter(lambda x: "study" in x, extracted_urls))

            # TODO query string, lowercase
            print(len(extracted_urls))
            # for url in extracted_urls:
            #     print(url)

            diff = set(extracted_urls).difference(self.result_urls)

            self.result_urls.update(diff)

            print(len(self.result_urls))

            print (len(diff))

            for url in diff:
                print(url)


            for url in list(diff):
                yield response.follow(url, callback=self.parse)



process = CrawlerProcess({
    "CONCURRENT_REQUESTS": 100,
    "REACTOR_THREADPOOL_MAXSIZE": 20,
    'LOG_LEVEL': 'INFO',
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
results = []

# def

# этоооооооооо
# dispatcher.connect(crawler_results, signal=signals.item_passed)

process.crawl(Spider, start_url ="http://teplo-seti.ru")
process.start()

# log.

log.start(logfile="results.log", loglevel=log.DEBUG, crawler=crawler, logstdout=False)

reactor.run()

with open("results.log", "r") as f:
    result = f.read()
print(result)