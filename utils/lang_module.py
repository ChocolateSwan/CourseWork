from PyDictionary import PyDictionary

dictionary=PyDictionary()


def find_synonyms_from_db(conn, words):
    """Поиск синонимов в БД или в API"""
    c = conn.cursor()
    synonyms = []
    for word in words:
        # Поиск в БД
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
        # Если поиск в БД не удался то через апишку
        if not arr:
            synonyms.append({"word":word, "synonyms": dictionary.synonym(word)})
        else:
            synonyms.append({"word":word, "synonyms": arr})
    c.close()
    return list(filter(lambda el: el['synonyms'], synonyms))
