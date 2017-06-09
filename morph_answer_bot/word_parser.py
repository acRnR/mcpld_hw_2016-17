from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()

with open('Narnia_words.txt', 'r', encoding='UTF-8') as b:
    wrds = b.read().split()

with open('Narnia_parsed.txt', 'w', encoding='UTF-8') as c:
    for item in wrds:
        ana = morph.parse(item)
        for el in ana:
            string = str(el.word) + '\t' + str(el.tag) + '\n'
            c.write(string)