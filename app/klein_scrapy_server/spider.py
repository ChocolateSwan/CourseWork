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
from spyder_utils import print_spider_info, find_words_on_page


class SpiderItem(scrapy.Item):
    url = scrapy.Field()
    found_arr = scrapy.Field()
    count = scrapy.Field()


class Spider(scrapy.Spider):
    name = "spider"

    def __init__(self, url="", word="", unwanted="", *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

        # TODO до ya.ru/sdsd/WE.WE
        self.allowed_domains = re.findall(r"https?://([\S]*\.[\w]{2,3})", url) or \
                               re.findall(r"^([\S]*\.[\w]{2,3})", url)
        self.root = re.findall(r"https?://([\S]*)", url) or \
                    [url]

        if word.find("|") == -1:
            self.words = word.split("*")
            self.separator = "*"
        else:
            self.words = word.split("|")
            self.separator = "|"

        self.result_urls = set()
        self.unwanted = unwanted.split()

        print_spider_info(self.start_urls, self.allowed_domains,
        self.root, self.separator, self.words, self.unwanted)


    def parse(self, response):

        print("Current url: ", response.url)

        has_unwanted_word = False

        # TODO по факту тут не надо искать по ссылкам и тд но хз
        for unwanted_word in self.unwanted:
            iteration_results = find_words_on_page(response, unwanted_word)
            if iteration_results:
                has_unwanted_word = True
                break

        print("Has unwanted words: {}".format(has_unwanted_word))
        #
        if not has_unwanted_word:
            yield response.follow(response.url, callback=self.parse_url)


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

    def parse_url(self, response):
        item = SpiderItem()
        item['url'] = response.url

        search_results = set()

        for word in self.words:
            iteration_results = find_words_on_page(response, word)

            if len(iteration_results) == 0 and self.separator == "*":
                search_results.clear()
                break
            else:
                search_results.update(iteration_results)

        item['found_arr'] = list(search_results)
        item['count'] = len(search_results)
        yield item
