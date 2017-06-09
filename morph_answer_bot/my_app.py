import random
from pymorphy2 import MorphAnalyzer
morph = MorphAnalyzer()


text = input('Введите что-нибудь: ')
wrds = []
arr = text.split()
for el in arr:
    if len(el) == 1:
        newl = el
    else:
        newl = el.strip('0123456789.,/\\;:\'"[]{}<>~`!@#$%?^&*()_+=-№')
    punct = ''
    if len(newl) != len(el):
        i = len(newl) - len(el)
        for item in range(i+1):
            punct += el[-i]
            i -= 1
    wrds.append([newl, punct])
lines = []
for wrd in wrds:
    al = []
    ana = morph.parse(wrd[0])[0]
    if 'UNKN' in ana.tag:
        print(wrd[0])
        wooord = wrd[0]
    else:
        tg = str(ana.tag)
        with open('Narnia_parsed.txt', 'r', encoding='UTF-8') as c:
            wds = c.read().split('\n')
            k = 0
            for w in wds:
                pair = w.split('\t')
                if len(pair) == 2 and k <= 15:
                    if pair[1] == tg and pair[0] != '':
                        al.append(pair[0])
                        k += 1
        wooord = random.choice(al)
    lines.append(str(wooord + wrd[1]))

phrase = ' '.join(lines)
print('\n', phrase)

