#!/usr/bin/python3
import json
from klein import route, run
from scrapy import signals
from scrapy.crawler import CrawlerRunner

from spider import Spider


class MyCrawlerRunner(CrawlerRunner):
    """
    Crawler object that collects items and returns output after finishing crawl.
    """
    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        # keep all items scraped
        self.items = []

        # create crawler (Same as in base CrawlerProcess)
        crawler = self.create_crawler(crawler_or_spidercls)

        # handle each item scraped
        crawler.signals.connect(self.item_scraped, signals.item_scraped)

        # create Twisted.Deferred launching crawl
        dfd = self._crawl(crawler, *args, **kwargs) #пробрасываем через кваргс word

        # add callback - when crawl is done cal return_items
        dfd.addCallback(self.return_items)
        return dfd

    def item_scraped(self, item, response, spider):
        self.items.append(item)

    def return_items(self, result):
        return self.items


def return_spider_output(output):
    """
    :param output: items scraped by CrawlerRunner
    :return: json with list of items
    """
    return json.dumps([dict(item) for item in output])


@route("/")
def schedule(request):
    word = request.args[b"word"][0]
    word = word.decode('utf-8')
    # url = request.args[b"url"][0]
    # url = url.decode('utf-8')
    url = "ww"
    runner = MyCrawlerRunner() #{"FEED_EXPORT_ENCODING":'utf-8'}
    spider = Spider() # Зачем он заходит в инит в этой строке и в строке dfd = self._crawl(crawler, *args, **kwargs)
    deferred = runner.crawl(spider, word=word, url=url)
    deferred.addCallback(return_spider_output)
    return deferred


run("localhost", 8900)

# TODO настройки в раннер
# process = CrawlerRunner({
#         "CONCURRENT_REQUESTS": 100,
#         "REACTOR_THREADPOOL_MAXSIZE": 20,
#         'LOG_LEVEL': 'INFO',
#         'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
#     })