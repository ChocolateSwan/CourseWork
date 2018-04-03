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
#linkextractor было
from scrapy.linkextractors import LinkExtractor
import scrapy
from urllib.parse import urljoin


class SpiderItem(scrapy.Item):
    url = scrapy.Field()
    found_arr = scrapy.Field()


class Spider(scrapy.Spider):
    name = "spider"
    # TODO: into params
    allowed_domains = ['teplo-seti.ru']
    visited_urls = []
    result_urls = set()

    # TODO: start_url to array
    # TODO allowed domains в конструктор
    def __init__(self, url=None, word="котел",  *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_urls = ["http://teplo-seti.ru"]
        self.word = word
        print (url, self.word)

    def parse(self, response):
        print("Current url: ", response.url)

        #Обработка текста
        # print(((response.body).decode()))
        resp_body = response.body.decode()
        # print(resp_body)
        print("результат поиска")
        # print(*list(re.findall(r'[^>]*тел[^<]*', resp_body)), sep="\n")
        search_results = response.xpath('//p/text()').re(r'\w*котел\w*')#.re(r'...кот...')


        if len(search_results):
            yield response.follow(response.url, callback=self.parse_result)
            print({response.url: search_results})
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
            # print(len(extracted_urls))
            # for url in extracted_urls:
            #     print(url)

            diff = set(extracted_urls).difference(self.result_urls)

            self.result_urls.update(diff)


# Раскомментировать!!!!!!!!!!
            # for url in list(diff):
            #     yield response.follow(url, callback=self.parse)

    #         TODO название
    def parse_result(self, response):
        item = SpiderItem()
        item['url'] = response.url
        # TODO Сделать set а то повторы
        item['found_arr'] = response.xpath('//p/text()').re(r'\w*котел\w*')
        yield item