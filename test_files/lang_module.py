from PyDictionary import PyDictionary
dictionary=PyDictionary()

CYRILLIC_SYMB = ('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')


# def find_synonyms(word):
#     return dictionary.synonym(word) or []

def find_synonyms(words):
    result = list(map (lambda el: {"word":el, "synonyms" :dictionary.synonym(el)}, words))
    return list(filter(lambda el: el['synonyms'], result))

def find_synonyms_from_db(conn, words):
    c = conn.cursor()
    synonyms = []
    for word in words:
        try:
            c.execute("""select
                      word1.word
                    from word word1
                    inner join synonym s on word1.word_id = s.first_word_id
                    inner join word word2 on word2.word_id = s.second_word_id
                    where word2.word = '{w}'
                    UNION 
                    select
                      word1.word
                    from word word1
                    inner join synonym s on word1.word_id = s.second_word_id
                    inner join word word2 on word2.word_id = s.first_word_id
                    where word2.word = '{w}'
                    ;""".format(w=word))
            arr = c.fetchall()
            arr = list(map(lambda x:x[0],arr))
        except:
            arr = []
        if not arr:
            synonyms.append({"word":word, "synonyms": dictionary.synonym(word)})
        else:
            synonyms.append({"word":word, "synonyms": arr})
    c.close()
    print(synonyms)
    return list(filter(lambda el: el['synonyms'], synonyms))



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






