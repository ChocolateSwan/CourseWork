import re


def print_spider_info(start_urls,
                      allowed_domains,
                      root,
                      separator,
                      words,
                      unwanted
                      ):
    """Вывод отладочной информации о краулере"""
    print("Start Spyder with:"
          " \n start urls: {},"
          " \n allowed_domains: {},"
          " \n root: {}, "
          " \n separator: {}"
          " \n words: {} "
          " \n unwanted words: {}".format(
                                    start_urls,
                                    allowed_domains,
                                    root,
                                    separator,
                                    words,
                                    unwanted),
    )


def find_words_on_page(response, word):
    """Поиск слова на станице"""
    # Первая буква слова заглавная или строчная
    reg_exp = r'\w*[' + re.escape(word[0].upper()) + \
              re.escape(word[0].lower()) + "]" + \
              re.escape(word[1:len(word)]) + r'\w*'
    iteration_results = response.xpath('//p/text()').re(reg_exp)
    iteration_results.extend(response.xpath('//li/text()').re(reg_exp))
    # iteration_results.extend(response.xpath('//a/text()').re(reg_exp))
    iteration_results.extend(response.xpath('//span/text()').re(reg_exp))
    iteration_results.extend(response.xpath('//h1/text()').re(reg_exp))
    iteration_results.extend(response.xpath('//h2/text()').re(reg_exp))
    iteration_results.extend(response.xpath('//h3/text()').re(reg_exp))
    return iteration_results
