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
import re


# class SpyderItem(scrapy.Item):
#     title = scrapy.Field()
#     body = scrapy.Field()
#     date = scrapy.Field()


class Spider(scrapy.Spider):
    name = "spider"
    # TODO: into params
    allowed_domains = ['www.ec-lyon.fr']
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
        if response.url not in self.visited_urls:
            self.visited_urls.append(response.url)
            # for post_link in response.xpath(
            #         '//div[@class="post mb-2"]/h2/a/@href').extract():
            #     url = response.url + post_link
            #     yield response.follow(url, callback=self.parse_post)
            # print (response.body)
            # print(response.xpath('//body').re(r'li.........'))
            # print(str(re.findall(r'ravoslovnotehn......', response.body)))
            next_pages = response.xpath(
                    '//a/@href').extract()
            # print (next_pages)
            # next_pages = filter(lambda x: "http" not in x and x not in ['/', '#'], next_pages)
            # next_pages = map(lambda x:urlparse.urljoin(response.url, x), next_pages )
            next_pages = self.validate_reference(next_pages, response.url)
            # print(*next_pages)
            # next_pages = map(lambda x: self.start_urls[0] + x, next_pages )
            # next_page = next_pages[1]
            print(len(next_pages))
            for url in next_pages:
                print(url)
            diff = set(next_pages).difference(self.result_urls)
            print(len(diff))
            self.result_urls.update(diff)

            for url in diff:
                print(url)
            print(len(self.result_urls))
            # yield response.follow(next_pages[0], callback=self.parse)

            mas_diff = list (diff)
            # for url in mas_diff:
            #     print ("qwertyuiop", url)
            #     yield response.follow(url, callback=self.parse)

            # next_page_url = + next_page
            # yield response.follow(next_page_url, callback=self.parse)

    def validate_reference(self, ref_list, url):
        ref_list = filter(lambda x: x not in ['/', '#'], ref_list)
        ref_list = map(lambda x: urljoin(url, x) if x[0:4] != "http" else x, ref_list)
        ref_list = filter(lambda x:self.val(x, url), ref_list)
        return list(ref_list)

    def val(self, ref, url):
        return self.allowed_domains[0] in ref and ref not in self.result_urls


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(Spider, start_url ="http://www.ec-lyon.fr")
process.start()