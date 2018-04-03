from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor

from .spider import RESULTS, Spider

process = CrawlerRunner({
        "CONCURRENT_REQUESTS": 100,
        "REACTOR_THREADPOOL_MAXSIZE": 20,
        'LOG_LEVEL': 'INFO',
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })


def pp(x):
    print(x)
    reactor.stop()

def run_spider(domain="test.ru", word="test"):

    process.crawl(Spider,
                  start_url="http://teplo-seti.ru",
                  word=word)
    # process.start()

    d = process.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.callFromThread(pp, 3)
    # reactor.run()

    return RESULTS
#
# print(run_spider())

