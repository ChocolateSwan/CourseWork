#!/usr/bin/python3
import json
from klein import route, run
from scrapy import signals
from scrapy.crawler import CrawlerRunner

from klein_config import (PORT,
                           HOST,
                           RUNNER_CONF)
from spider import Spider


class MyCrawlerRunner(CrawlerRunner):
    """ Собирает itemы и возвращает результаты после окончания работы краулера"""
    def crawl(self, crawler_or_spidercls, *args, **kwargs):
        """Настройка работы краулера"""
        # Все собранные itemы
        self.items = []

        # Создание краулера
        crawler = self.create_crawler(crawler_or_spidercls)

        # Перехват каждого собранного item
        crawler.signals.connect(self.item_scraped, signals.item_scraped)

        # Создание Twisted.Deferred стартующего краулинг
        dfd = self._crawl(crawler, *args, **kwargs)

        # Когда краулинг окончен вызывается return_items
        dfd.addCallback(self.return_items)
        return dfd

    def item_scraped(self, item):
        """Перехват item и добавление его в список"""
        self.items.append(item)

    def return_items(self, result):
        """Возврат всего собранного"""
        return self.items


def return_spider_output(output):
    """После краулинга возвращает список itemов из краулера"""
    return json.dumps([dict(item) for item in output])


@route("/")
def schedule(request):
    """Обработка запроса к краулеру"""
    # Слова
    word = request.args[b"word"][0]
    word = word.decode('utf-8')
    # Урл
    url = request.args[b"url"][0]
    url = url.decode('utf-8')
    # Нежелательные термины
    unwanted = request.args[b"unwanted"][0]
    unwanted = unwanted.decode('utf-8')
    runner = MyCrawlerRunner(RUNNER_CONF)
    spider = Spider()
    deferred = runner.crawl(spider, word=word, url=url, unwanted=unwanted)
    deferred.addCallback(return_spider_output)
    return deferred


run(HOST, PORT)
