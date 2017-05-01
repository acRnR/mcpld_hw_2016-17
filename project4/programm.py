import os
import re


def inp_dirs():
    mstm_path = input('путь к майстему:\n')
    inp_name = input('имя файла с текстом:\n')
    outp_name = input('имя файла с результатами майстема:\n')
    ins_name = input('имя файла с инсертами:\n')
    return mstm_path, inp_name, outp_name, ins_name


def mystem_go(inp1, inp2, inp3):
    mystem_path = inp1 + " -nd "
    m_command = mystem_path + inp2 + " " + inp3
    os.system(m_command)


def find_sec(l):
    res = re.search('(.+?)\{(.+?)}', l)
    word = res.group(1)
    lemma = res.group(2)
    return word, lemma


def find_fir(l):
    arr = l.split()
    w_arr = []
    punct = '&%\\;="/.:()\#,_!?\'©{}$+|'
    for el in arr:
        el = el.strip('\ufeff\t')
        w = el.strip(punct)
        for sym in punct:
            el = el.replace(sym, (' ' + sym + ' '))
            el = el.replace('  ', '')
            wp_block = el.split()
            if wp_block[0] == w:
                wp_block.insert(0, '')
            if len(wp_block) == 2:
                wp_block.append('')
        w_arr.append(wp_block)
    return w_arr


def l_check(l):
    line = l.split()
    a_id = line[7].strip('"(,')
    w = line[8].strip(',"')
    l = line[9].strip(',)"')
    return a_id, w, l


def make_second(ou, fw):
    fr = open(ou, 'r', encoding='UTF-8')
    raw = 'insert into analys (id, word, lemma) values (%d, "%s", "%s")\n'
    fn = open(fw,  'w', encoding='UTF-8')
    n = 0
    wl_set = set()
    for line in fr:
        pair = find_sec(line)
        wl_set.add(pair)
    for el in wl_set:
        n += 1
        w = el[0]
        l = el[1]
        fn.write(raw % (n, w, l))
    fr.close()
    fn.close()
    return fn


def make_first(inp, insdb):
    sec = open(inp, 'r', encoding='UTF-8')
    fr = open(insdb, 'r', encoding='UTF-8')
    raw = 'insert into words (id, analys_id, l_punct, word, r_punct, lemma) values (%d, %s, "%s", "%s", "%s", "%s")\n'
    n = 1
    seq = []
    a = sec.read()
    b = fr.readlines()
    arr = find_fir(a)
    for el in arr:
        for lin in b:
            a_info = l_check(lin)
            if el[1] == a_info[1]:
                a_id = a_info[0]
                lemma = a_info[2]
                seq.append((n, a_id, el[0], el[1], el[2], lemma))
                break
        n += 1
    sec.close()
    fr.close()
    fw = open(insdb, 'a', encoding='UTF-8')
    for i in seq:
        fw.write(raw % i)
    fw.close()


def main():
    mstm_path, inp_name, outp_name, ins_name = inp_dirs()

    mystem_go(mstm_path, inp_name, outp_name)
    make_second(outp_name, ins_name)
    make_first(inp_name, ins_name)

if __name__ == '__main__':
    main()