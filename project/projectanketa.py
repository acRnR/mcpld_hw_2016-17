from flask import Flask
from flask import url_for, render_template, request, redirect
import json


app = Flask(__name__)

def make_head():
    #создает вспомагательный файл, в который для дальнейшего использования будет скидываться введенная информация, и делает в нем шапку
    head = 'name\tstudy\torth1\torth2\torth3\torth4\torth5\torth6\torth7\torth8\torth9\torth10\tlex1\tlex2\tlex3\tlex4\tlex5\tlex6\tlex7\tlex8\tlex9\tlex10\n'
    f = open('backup.txt', 'w', encoding='UTF-8')
    f.write(head)
    f.close()

def data_stat():
    #собирает из файла backup введенные данные и анализирует их для того, чтобы вывести их
    #в stats, на странице со статистикой
    f = open('backup.txt', 'r', encoding='UTF-8')
    for_table = [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]
    res_n = 0
    for line in f:
        if 'orth' in line:
            continue
        res_n += 1
        arr = line.split('\t')
        functions = [our_or(arr), gue_g(arr), re_er(arr), ise_ize(arr), random_orth(arr), lex_tran(arr), lex_radio(arr)]
        for i in range(len(for_table)):
            for_table[i][0] += functions[i][0]
            for_table[i][1] += functions[i][1]
            i += 1

    f.close()
    #for_table - массив с массивами с кол-вом вхождений Брит[0]/Амер[1] вариантов слов для каждого столбца таблицы
    return for_table, res_n

def our_or(arr):
    #Британский вариант favourite colour, Американский вариант favorite color
    a = [arr[5], arr[11]]
    brit = 0
    amer = 0
    for el in a:
        if 'our' in el:
            brit += 1
        elif 'or' in el:
            amer += 1
    return brit, amer

def gue_g(arr):
    #Британский вариант dialogue catalogue, Американский вариант dialog catalog
    a = [arr[2], arr[4]]
    brit = 0
    amer = 0
    for el in a:
        if 'gue' in el:
            brit += 1
        elif el[len(el)-1] == 'g':
            amer += 1
    return brit, amer

def random_orth(arr):
    #Британский вариант defence gray, Американский вариант defense grey
    a = [arr[3], arr[8]]
    brit = 0
    amer = 0
    for el in a:
        if 'ence' in el or 'ay' in el:
            brit += 1
        elif 'ense' in el or 'ey' in el:
            amer += 1
    return brit, amer

def re_er(arr):
    #Британский вариант theatre centre, Американский вариант theater center
    a = [arr[9], arr[10]]
    brit = 0
    amer = 0
    for el in a:
        if 're' in el:
            brit += 1
        elif 'er' in el:
            amer += 1
    return brit, amer

def ise_ize(arr):
    #Британский вариант organise recognise, Американский вариант organize recognize
    a = [arr[7], arr[8]]
    brit = 0
    amer = 0
    for el in a:
        if 'ise' in el:
            brit += 1
        elif 'ize' in el:
            amer += 1
    return brit, amer

def lex_tran(arr):
    #Брит: flat rubber lift rubbish queue post timetable torch
    #Амер: appartment eraser elevator trash/garbage line mail scedule flashlight
    a = [arr[12], arr[13], arr[14], arr[15], arr[16], arr[17], arr[18], arr[19]]
    brit = 0
    amer = 0
    for el in a:
        if el == 'flat' or 'rub' in el or  el == 'lift' or 'que' in el or el == 'post' or 'time' in el or 'tor' in el:
            brit += 1
        elif 'part' in el or el[0] == 'e' or 'tra' in el or 'garb' in el or el == 'line' or el == 'mail' or 'dule' in el or 'light' in el:
            amer += 1
    return brit, amer

def lex_radio(arr):
    #Британское bathroom - ванная комната, американское - туалет
    #Британское chips - жаренная "картошка фри", американское - чипсы
    a = [arr[20], arr[21]]
    brit = 0
    amer = 0
    for el in a:
        if el[2] == 'b':
            brit += 1
        if el[2] == 'a':
            amer += 1
    return brit, amer

def data_search(parameter, place):
    #Ищет в таблице backup строки с введенными при поиске данными
    #имя/факт целенаправленного (не)обучения американскому английскому
    f = open('backup.txt', 'r', encoding='UTF-8')
    res = []
    for line in f:
        if 'orth' in line:
            continue
        arr = line.split('\t')
        if arr[place] == parameter:
            res.append(arr)
    f.close()
    #возвращает список со списками слов тех строк, которые подходят по параметрам поиска
    return res


@app.route('/')
def index():
    #Анкета
    #параметр "автозаполнение" отключен, чтобы не было лишних
    #подсказок, отвлекающих респондента от его лингвистического чутья
    fi = open('backup.txt', 'a', encoding='UTF-8')
    if request.args:
        name = request.args['name']
        study = request.args['study']
        or1 = request.args['ortho1']
        or2 = request.args['ortho2']
        or3 = request.args['ortho3']
        or4 = request.args['ortho4']
        or5 = request.args['ortho5']
        or6 = request.args['ortho6']
        or7 = request.args['ortho7']
        or8 = request.args['ortho8']
        or9 = request.args['ortho9']
        or10 = request.args['ortho10']
        lex1 = request.args['lex1']
        lex2 = request.args['lex2']
        lex3 = request.args['lex3']
        lex4 = request.args['lex4']
        lex5 = request.args['lex5']
        lex6 = request.args['lex6']
        lex7 = request.args['lex7']
        lex8 = request.args['lex8']
        lex9 = request.args['lex9']
        lex10 = request.args['lex10']

        fi.write(name+'\t'+study+'\t'+or1+'\t'+or2+'\t'+or3+'\t'+or4+'\t'+or5+'\t'+or6+'\t'+or7+'\t'+or8+'\t'+or9+'\t'+or10+'\t'+lex1+'\t'+lex2+'\t'+lex3+'\t'+lex4+'\t'+lex5+'\t'+lex6+'\t'+lex7+'\t'+lex8+'\t'+lex9+'\t'+lex10+'\n')
        fi.close()
        return redirect('stats')
    return render_template('index.html')

@app.route('/stats')
def stats():
    #статистика
    #Выводятся данные, полученные в data_stat() 
    again_refer = url_for('index')
    search_refer = url_for('sear')
    json_refer = url_for('jsonres')
    t, n = data_stat()
    return render_template('statistics.html',n=n, again_refer=again_refer, search_refer=search_refer, json_refer=json_refer, our_n=t[0][0], gue_n=t[1][0], re_n=t[2][0], ise_n=t[3][0], randombr_n=t[4][0], lex1br_n=t[5][0], lex2br_n=t[6][0], or_n=t[0][1], g_n=t[1][1], er_n=t[2][1], ize_n=t[3][1], randomam_n=t[4][1], lex1am_n=t[5][1], lex2am_n=t[6][1])

@app.route('/json')
def jsonres():
    #выводит данные в json формате
    again_refer = url_for('index')
    search_refer = url_for('sear')
    stats_refer = url_for('stats')

    d = dict(name=[], study=[], ort1=[], ort2=[], ort3=[], ort4=[], ort5=[], ort6=[], ort7=[], ort8=[], ort9=[], ort10=[], le1=[], le2=[], le3=[], le4=[], le5=[], le6=[], le7=[], le8=[], le9=[], le10=[])
    fil = open('backup.txt', 'r', encoding='UTF-8')
    for line in fil:
        if 'orth' in line:
            continue
        arr = line.split('\t')
        d['name'].append(arr[0])
        d['study'].append(arr[1])
        d['ort1'].append(arr[2])
        d['ort2'].append(arr[3])
        d['ort3'].append(arr[4])
        d['ort4'].append(arr[5])
        d['ort5'].append(arr[6])
        d['ort6'].append(arr[7])
        d['ort7'].append(arr[8])
        d['ort8'].append(arr[9])
        d['ort9'].append(arr[10])
        d['ort10'].append(arr[11])
        d['le1'].append(arr[12])
        d['le2'].append(arr[13])
        d['le3'].append(arr[14])
        d['le4'].append(arr[15])
        d['le5'].append(arr[16])
        d['le6'].append(arr[17])
        d['le7'].append(arr[18])
        d['le8'].append(arr[19])
        d['le9'].append(arr[20])
        d['le10'].append(arr[21].strip())
    fil.close()
    data = json.dumps(d, sort_keys=True, ensure_ascii=False, indent=4, separators=(',\n', ':'))
    return render_template('jsonres.html', again_refer=again_refer, search_refer=search_refer, stats_refer=stats_refer, data=data)

@app.route('/search')
def sear():
    #поиск по введенным данным
    #поиск возможен по имени ИЛИ по факту
    #целенаправленного (не)обучения американскому английскому
    if request.args:
        return redirect('results')
    return render_template('search.html')

@app.route('/results')
def results():
    #результаты поиска по введенным данным
    again_refer = url_for('index')
    search_refer = url_for('sear')
    stats_refer = url_for('stats')
    json_refer = url_for('jsonres')

    study = request.args['searchstudy']
    name = request.args['searchname']

    if study != 'byname':
        arr = data_search(study, 1)
    elif study == 'byname':
        arr = data_search(name, 0)
    return render_template('results.html', again_refer=again_refer, search_refer=search_refer, stats_refer=stats_refer, json_refer=json_refer, arr=arr)#, q2=q2, q1=q1)#, #letstry = ln)

if __name__ == '__main__':
    #make_head()
    app.run(debug=True)
