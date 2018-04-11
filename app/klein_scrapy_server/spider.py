# -*- coding: utf-8 -*-
# python 3
"""
scrapy crawl pycoder -a start_url=http://www.dmu.ac.uk
or
python3 ./...
"""

from scrapy.linkextractors import LinkExtractor
import scrapy
import re


class SpiderItem(scrapy.Item):
    url = scrapy.Field()
    found_arr = scrapy.Field()


class Spider(scrapy.Spider):
    name = "spider"
    # TODO: into params
    visited_urls = []
    result_urls = set()

    def __init__(self, url="", word="",  *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        # TODO до ya.ru/sdsd/WE.WE
        self.allowed_domains = re.findall(r"https?://([\S]*\.[\w]{2,3})", url) or \
                               re.findall(r"^([\S]*\.[\w]{2,3})", url)
        self.root = re.findall(r"https?://([\S]*)", url) or \
                    [url]
        self.word = word
        print("Srart Spyder with:"
              " \n start urls: {},"
              " \n allowed_domains: {},"
              " \n root: {},"
              " \n word: {} ".format(
                    self.start_urls,
                    self.allowed_domains,
                    self.root,
                    self.word),
              )

    def parse(self, response):
        print("Current url: ", response.url)

        #Обработка текста
        # print(((response.body).decode()))
        resp_body = response.body.decode()

        search_results = response.xpath('//p/text()').re(r'\w*' + re.escape(self.word) + r'\w*')

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
            extracted_urls = list(filter(lambda x: self.root[0] in x, extracted_urls))
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
        item['found_arr'] = response.xpath('//p/text()').re(r'\w*' + re.escape(self.word) + r'\w*')

        yield item


 # TODO заранее собрать регулярку