# -*- coding: utf-8 -*-
# python 3

import re
from scrapy.linkextractors import LinkExtractor
import scrapy

from spyder_utils import (print_spider_info,
                          find_words_on_page)


class SpiderItem(scrapy.Item):
    """Результат поиска одной страницы"""
    url = scrapy.Field()
    found_arr = scrapy.Field()
    count = scrapy.Field()


class Spider(scrapy.Spider):
    """Краулер для поиска слов на страницах"""
    name = "spider"

    def __init__(self, url="", word="", unwanted="", *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

        self.allowed_domains = re.findall(r"https?://([^/]*\.[\w]{2,3})", url) or \
                               re.findall(r"^([^/]*\.[\w]{2,3})", url)
        self.root = re.findall(r"https?://([\S]*)", url) or [url]

        if word.find("|") == -1:
            self.words = word.split("*")
            self.separator = "*"
        else:
            self.words = word.split("|")
            self.separator = "|"

        self.result_urls = set()
        self.visited_urls = set()

        self.unwanted = unwanted.split()

        print_spider_info(self.start_urls, self.allowed_domains,
            self.root, self.separator, self.words, self.unwanted)

    def parse(self, response):
        """ Обработка страницы"""
        url_without_scheme = re.findall(r"https?://([\w/.-]*)", response.url)[0]

        # Чтобы урлы не повторялись
        if url_without_scheme not in self.visited_urls:

            self.result_urls.add(response.url.lower())
            self.visited_urls.add(url_without_scheme.lower())

            # Поиск нежелательных терминов на странице
            has_unwanted_word = False

            for unwanted_word in self.unwanted:
                iteration_results = find_words_on_page(response, unwanted_word)
                if iteration_results:
                    has_unwanted_word = True
                    break

            # Если на странице нет нежелательных терминов, то обрабатываем
            if not has_unwanted_word:
                item = SpiderItem()
                item['url'] = response.url
                # Поиск результатов
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

            # Поиск урлов на странице
            link_extractor = LinkExtractor()
            extracted_urls = link_extractor.extract_links(response)
            extracted_urls = list(map(lambda link: link.url, extracted_urls))
            extracted_urls = list(filter(lambda x: x.rfind("#") < x.rfind("/"), extracted_urls))
            extracted_urls = list(filter(lambda x: self.allowed_domains[0] in x, extracted_urls))
            extracted_urls = list(filter(lambda x: self.root[0] in x, extracted_urls))
            extracted_urls = list(map(lambda x: x[0:x.rfind("?")] if x.rfind("?") > x.rfind("/") else x, extracted_urls))

            # Чтобы не было повторов страниц с из-за регистра букв
            extracted_urls = list(map(lambda u: u.lower(),extracted_urls))

            # Урлы которые еще не учитывались
            diff = set(extracted_urls).difference(self.result_urls)
            # Учитываем и их
            self.result_urls.update(diff)
            # Рекурсивно по новым урлам
            for url in list(diff):
                yield response.follow(url, callback=self.parse)
