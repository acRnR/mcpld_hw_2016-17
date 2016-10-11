import urllib.request
import re
import os
import time

def kill(path):
    if len(os.listdir(path))==0:
        os.rmdir(path)
        print(path)

def kill_cycle():
    folders = ['plain', 'mystem-xml', 'mystem-plain']
    for fol in folders:
        for year in range(2009, 2017):
            for month in range(1, 13):
                row = './Istoki-Bashkortostan/%s/%d/%d'
                adress = row % (fol, year, month)
                kill(adress)
            n_row = './Istoki-Bashkortostan/%s/%d'
            n_adr = n_row % (fol, year)
            kill(n_adr)

def header_off(path):
    f = open(path, 'r', encoding='UTF-8')
    
    lst = f.readlines()
    lines = lst[6:]
    fi = open('./Istoki-Bashkortostan/noheader.txt', 'w', encoding='UTF-8')
    for line in lines:
        fi.write(line)
    f.close()
    fi.close()

def command(line):
    row1 = r"C:\Users\ssimo\Documents\mkold\mystem.exe -cid "
    row2 = r"C:\Users\ssimo\Documents\mkold\mystem.exe -cid --format xml "
    li = line.split('\t')
    inp = li[0]
    header_off(inp)
    no_header = './Istoki-Bashkortostan/noheader.txt'
    if inp == 'path':
        return 'Nope'
    else:
        inp = inp.replace('/', '\\')
        no_header = no_header.replace('/', '\\')
        outp_plain = inp.replace('plain', 'mystem-plain')
        outp_xml = outp_plain.replace('-plain', '-xml')
        outp_xml = outp_xml.replace('.txt', '.xml')
        com1 = row1 + no_header + " " +  outp_plain
        com2 = row2 + no_header + " " + outp_xml
        return com1, com2


def mystem():
    print('markup in progress')
    f = open('./Istoki-Bashkortostan/metadata.csv', 'r', encoding='UTF-8')
    lst = f.readlines()
    lines = lst[1:]
    f.close()
    i = 0
    for line in lines:
        rawcom = command(line)
        if rawcom == 'Nope':
            continue
        print (i)
        i += 1
        com1 = rawcom[0]
        com2 = rawcom[1]
        os.system(com1)
        os.system(com2)
    print('markup done')

    
def add_csv(way, year):
    #print('way', way)
    fi = open(way, 'r', encoding = 'UTF-8')
    arr = fi.read()
    res = re.search('@au (.+?)\n@ti (.+?)\n@da (.+?)\n@topic (.+?)\n@url (.+?)\n', arr)
    info = res.group(1, 2, 3, 4, 5)
    #print(info)
    fi.close()
    f = open('Istoki-Bashkortostan/metadata.csv', 'a', encoding = 'UTF-8')
    row = '%s\t%s\t\t\t%s\t%s\tпублицистика\t\t\t%s\t\tнейтральный\tн-возраст\tн-уровень\tреспубликанская\t%s\tИстоки\t\t%s\tгазета\tРоссия\tреспублика Башкорстостан\tru\n'
    f.write(row % (way, info[0], info[1], info[2], info[3], info[4], year))
    f.close()

def make_csv():
    f = open('./Istoki-Bashkortostan/metadata.csv', 'a', encoding = 'UTF-8')
    f.write('path\tauthor\tsex\tbirthday\theader\tcreated\tsphere\tgenre_fi\ttype\ttopic\tchronotop\tstyle\taudience_age\taudience_size\tsource\tpublication\tpublisher\tpubl_year\tmedium\tcountry\tregion\tlanguage\n')
    f.close()

def clean(t):
    #очищает тексты статей от ненужных символов
    rg = re.compile('&nbsp;&nbsp;&nbsp;\t\t(.+?)</div>', flags=re.DOTALL)
    res = re.search(rg, t)
    main_part = res.group(1)
    reg_tag = re.compile('<.*?>', flags=re.DOTALL)
    no_tag = reg_tag.sub("", main_part)
    #no_sign = ''
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

def get_author(t):
    res = re.search('<img src=\'images/author.jpg\' style=.+?>(.+?)</div>', t)
    auth = res.group(1)
    auth = auth.strip(' ')
    auth = auth.strip('\t')
    if auth == 'Собственный корреспондент':
        auth = 'None'
    #print('author is allright')
    return auth

def get_title(t):
    #rg = re.compile('.*?', flags=re.DOTALL)
    res = re.search("<div class='title'>\r\n(.*?)</div>", t)
    title = res.group(1)
    title = title.strip(' ')
    title = title.strip('\t')
    #print('title ok')
    return title

def get_topic(t):
    res = re.search('<div class=\'razdel\'>(.*?)</div>', t)
    topic = res.group(1)
    topic = topic.strip('\t ')
    #print('topic ok')
    return topic


def get_text(text, remember):
    #собирает все необходимые данные
    print('collect & clean', end=' ')
    auth = get_author(text)
    title = get_title(text)
    da = get_date(text)
    top = get_topic(text)
    url = remember
    clean_t = clean(text)
    row = '@au %s\n@ti %s\n@da %s\n@topic %s\n@url %s\n\n%s'
    plain_t = row % (auth, title, da, top, url, clean_t)
    #print('clean af', end = ' ')
    return plain_t


def get_date(t):
    # приводит даты к общему, нужному нам, виду
    date = ''
    month = {
        'Января,' : '01',
        'Февраля,' : '02',
        'Марта,' : '03',
        'Апреля,' : '04',
        'Мая,' : '05',
        'Июня,' : '06',
        'Июля,' : '07',
        'Августа,' : '08',
        'Сентября,' : '09',
        'Октября,' : '10',
        'Ноября,' : '11',
        'Декабря,' : '12'
        }
    res = re.search('src=\'images/clock.jpg\' style=\'.+?;\'>(.+?)</div>', t)
    raw_date = res.group(1)
    raw_date = raw_date.strip(' \t')
    if '.' in raw_date:
        date = raw_date
    else:
        date_l = raw_date.split(' ')
        date_l[1] = month[date_l[1]]
        for el in date_l:
            date += el + '.'
        date = date.strip('.')
    return date


def get_html(url):
    # на сайте много страниц, которые вроде существуют, но статей на них нет.
    # зато есть фраза "Элемент не найден!", по которой можно определить ненужные
    # нам страницы и не тратить на них время
    remember_url = ''
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
    req = urllib.request.Request(url, headers={'User-Agent':user_agent})
    with urllib.request.urlopen(req) as response:
        html = response.read().decode('utf-8')
    if 'Элемент не найден!' in html:
        return 'Nope'        
    else:
        remember_url = url
        date = get_date(html)
        plain_t = get_text(html, remember_url)
        print('item', end=' ')
        return plain_t, date
    
    for n in range(2187, 3750):#вообще статей аж до номера 5203, но для пробы достаточно будет двух
        row = 'http://istoki-rb.ru/archive.php?article=%d'
        n_url = row % n

        try:
            answer = get_html(n_url)
            if answer != 'Nope':
                print(n)
                csv_plain(answer)
        except:
            print('ERROR')
            time.sleep(3)
            answer = get_html(n_url)
            if answer != 'Nope':
                print(n)
                csv_plain(answer)


def make_dir(d_name):
    if not os.path.exists(d_name):
        os.makedirs(d_name)


def all_dirs():
    #создает все необходимые директории
    folders = ['plain', 'mystem-xml', 'mystem-plain']
    for fol in folders:
        for year in range(2009, 2017):
            for month in range(1, 13):
                row = './Istoki-Bashkortostan/%s/%d/%d'
                adress = row % (fol, year, month)
                make_dir(adress)
    print('directories')
    
def main():
    #all_dirs()
    #make_csv()
    #create_dict()
    #mystem()
    kill_cycle()

if __name__=='__main__':
    main()


