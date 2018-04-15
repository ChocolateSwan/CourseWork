from PyDictionary import PyDictionary
dictionary=PyDictionary()

CYRILLIC_SYMB = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')


# def find_synonyms(word):
#     return dictionary.synonym(word) or []

def find_synonyms(words):
    result = list(map (lambda el: {"word":el, "synonyms" :dictionary.synonym(el)}, words))
    return list(filter(lambda el: el['synonyms'], result))


def find_antonyms(words):
    result = list(map(lambda el: {"word": el, "antonyms": dictionary.antonym(el)}, words))
    return list(filter(lambda el: el['antonyms'], result))


def has_cyrillic_symb(word):
    return [x for x in CYRILLIC_SYMB if x in word.lower()]

def traslate(word):
    if word.find("|") == -1:
        words = word.split("*")
        separator = "*"
    else:
        words = word.split("|")
        separator = "|"
    print(words, separator)
    # words = list(map(lambda w: dictionary.translate(w, 'en')
    #                     if len(w) == len(has_cyrillic_symb(w))
    #                         else w, words))

    words = list(map(lambda w: dictionary.translate(w, 'en'), words))
    words = list(filter(lambda w: w, words))
    print(words)
    return separator.join(words)

# print(traslate("собака*кошка*лошадь"))






