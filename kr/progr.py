import os
import re
import json
from flask import Flask
from flask import url_for, render_template, request, redirect


app = Flask(__name__)


def na_5():
    d = {}
    for root, dirs, files in os.walk('.'):
        for fl in files:
            if 'lexemes' in fl:
                f = open(fl, 'r', encoding='UTF-8')
                a = f.read().split('\n\n')
                for el in a:
                    k, v = str_to_dict(el)
                    d[k] = v
                f.close()
    return d


def str_to_dict(arr):
    rg = re.compile('-lexeme\n lex:(.+?)\n stem:.+?\n gramm: (.+?)\n paradigm:.+?\n trans_ru: (.+)', flags=re.DOTALL)
    res = re.search(rg, arr)
    try:
        k = res.group(1).strip()
    except AttributeError:
        k = ''
    try:
        pos = res.group(2)
    except AttributeError:
        pos = ''
    try:
        rtr = res.group(3)
    except AttributeError:
        rtr = ''
    value = (pos, rtr)
    return k, value


def na_8(d):
    data = json.dumps(d, sort_keys=True, ensure_ascii=False, indent=4, separators=(',\n', ':'))
    f = open('udm_to_rus.txt', 'w', encoding='UTF-8')
    f.write(data)
    f.close()
    newd = {}
    for key in d:
        kk, vv = new_d(key, d[key])
        for k in kk:
            newd[k] = vv
    new_data = json.dumps(newd, sort_keys=True, ensure_ascii=False, indent=4, separators=(',\n', ':'))
    f1 = open('rus_to_udm.txt', 'w', encoding='UTF-8')
    f1.write(new_data)
    f1.close()


def new_d(k, v):
    keys = v[1].split(', ')
    val = (k, v[0])
    return keys, val


@app.route('/')
def index():
    if request.args:
        return redirect('result')
    return render_template('index.html')


@app.route('/result')
def result():
    again_refer = url_for('index')
    req = request.args['req']
    a = 0
    print(di)
    if req in di:
        print('lf')
        response = di[req]
    else:
        a = 1
        response = 'Такое слово не найдено в нашем словаре, попробуйте другое'
    return render_template('result.html', again_refer=again_refer, response=response, a=a)


if __name__ == '__main__':
    di = na_5()
    na_8(di)
    app.run()
