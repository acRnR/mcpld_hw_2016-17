import os
import re


def mystem_go():
    mystem_path = r"C:\Users\ssimo\Documents\mkold\mystem.exe -nd "
    inp_name = "inp.txt"
    outp_name = "outp.txt"
    m_command = mystem_path + inp_name + " " + outp_name
    os.system(m_command)
    return outp_name


def find_sec(l):
    res = re.search('(.+?)\{(.+?)}', l)
    word = res.group(1)
    lemma = res.group(2)
    return word, lemma


def find_fir(l):



def make_second(ou):
    fr = open(ou, 'r', encoding='UTF-8')
    raw = 'insert into one(id, word, lemma) values(%d, %s, %s)\n'
    fn = open('ins_for_db.txt',  'w', encoding='UTF-8')
    n = 0
    for line in fr:
        n += 1
        w, l = find_sec(line)
        fn.write(raw % (n, w, l))
    fr.close()
    fn.close()
    return fn


def make_first(fi):
    sec = open(fi, 'r', encoding='UTF-8')
    n = 0
    for line in sec:
        pass
        n += 1
        i, w, l = fin
    pass

def main():
    outp = mystem_go()
    make_second(outp)

if __name__ == '__main__':
    main()