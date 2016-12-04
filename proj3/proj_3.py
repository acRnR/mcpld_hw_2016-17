import urllib.request
import re
import os


ts_g = re.compile('definition-text--left-margin">(.+?)<p>ЧИТАЙТЕ ТАКЖЕ:</p>', flags=re.DOTALL)
ria_f = re.compile('title="Ученые создали лекарство от слепоты"></p>\n\n<p><strong>(.+?)<div', flags=re.DOTALL)
na_ne = re.compile('title="Ученые создали вакцину, которая сможет вернуть зрение слепым"></p>(.+?)<script', flags=re.DOTALL)
ru_ec = re.compile('<figcaption>(.+?)<p style=', flags=re.DOTALL)
d = {
    'http://tsargrad.tv/news/2016/12/04/odin-ukol-vernet-zrenie-uchenye': ts_g,
    'https://riafan.ru/581023-uchenye-sozdali-lekarstvo-ot-slepoty': ria_f,
    'https://nation-news.ru/229133-uchenye-sozdali-vakcinu-kotoraya-smozhet-vernut-zrenie-slepym': na_ne,
    'https://rueconomics.ru/210954-uchenye-podobralis-k-sozdaniyu-vakciny-ot-slepoty': ru_ec
}


def get_html(url):
#заходит на страницы
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(url, headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    return html


def write_file():
    i = 0
    f_name = './articles/article_%d.txt'
    for key in d:
        t = get_html(key)
        i += 1
        nam = f_name % i
        res = re.search(d[key], t)
        r_text = res.group(1)
        text = clean(r_text)
        new_f = open(nam, 'w', encoding='UTF-8')
        new_f.write(text.strip())
        new_f.close()


def clean(t):
    #очищает тексты статей от ненужных символов
    reg_tag = re.compile('<.*?>', flags=re.DOTALL)
    no_tag = reg_tag.sub("", t)
    signs = {
        '&laquo;' : '«',
        '&raquo;' : '»',
        '&ndash;' : '–',
        '&mdash;' : '—',
        '&hellip;' : '…',
        '&bull;' : '•',
        '&ldquo;' : '“',
        '&rdquo;' : '”',
        '&#40;' : '(',
        '&#41;' : ')',
        '&#37;' : '%'
        }
    for s in signs:
        no_tag = no_tag.replace(s, signs[s])
    return no_tag


def makes_sets():
    f_name = './articles/article_%d.txt'
    sets = []
    for n in range(4):
        n += 1
        nam = f_name % n
        f = open(nam, 'r', encoding='UTF-8')
        arr = f.read().split()
        n_ar = []
        for word in arr:
            n_w = word.strip('.,!?:;_-– []()\|/\n 1234567890«»')
            if n_w != '':
                n_ar.append(n_w.lower())
        sets.append(set(n_ar))
        f.close()
    return sets


def compare(sets):
    int_sect = sets[0] & sets[1] & sets[2] & sets[3]
    n2 = ((sets[0] & sets[1]) | (sets[2] & sets[3])) | ((sets[0] & sets[3]) | (sets[1] & sets[2])) | (sets[0] & sets[2]) | (sets[1] & sets[3])
    n0 = sets[0] | sets[1] | sets[2] | sets[3]
    sym_dif = n0 - n2
    #write_info(int_sect, sym_dif)
    return int_sect, sym_dif


def write_info(inf1, inf2):
    f1 = open('./info/пересечение.txt', 'w', encoding='UTF-8')
    f2 = open('./info/симм_разность.txt', 'w', encoding='UTF-8')
    arr1 = sorted(list(inf1))
    arr2 = sorted(list(inf2))
    for word in arr1:
        f1.write(word + '\n')
    f1.close()
    for wor in arr2:
        f2.write(wor + '\n')
    f2.close()


def main():
    #write_file()
    w1, w2 = compare(makes_sets())
    write_info(w1, w2)

if __name__=='__main__':
    main()
