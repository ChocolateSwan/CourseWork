# from langdetect import detect
# from langdetect import detect_langs
# print(detect_langs('Ты говоришь на "мові"'))


import cld2

# текст на Русском
details = cld2.detect("hello every body")
print(str(details))

# Вывод:
# Detections(is_reliable=True, bytes_found=43, details=(Detection(language_name='RUSSIAN', language_code='ru', percent=97, score=658.0), Detection(language_name='Unknown', language_code='un', percent=0, score=0.0), Detection(language_name='Unknown', language_code='un', percent=0, score=0.0)))

# текст на Украинском
# details = cld2.detect("Це мій зразок тексту")
