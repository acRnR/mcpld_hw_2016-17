import os
import re


def mystem_go():
    mystem_path = r"C:\Users\ssimo\Documents\mkold\mystem.exe -nd "
    inp_name = "inp.txt"
    outp_name = "outp.txt"
    m_command = mystem_path + inp_name + " " + outp_name
    os.system(m_command)
    return outp_name


def find_words(l):
    res = re.search('(.+?)\{(.+?)}', l)
    word = res.group(1)
    lemma = res.group(2)
    return word, lemma


def make_ins(ou):
    fr = open(ou, 'r', encoding='UTF-8')
    #f = fr.read()
    raw = 'insert into one(word, lemma) values(%s, %s)\n'
    fn = open('ins_for_db.txt',  'a', encoding='UTF-8')
    for line in fr:
        w, l = find_words(line)
        fn.write(raw % (w, l))
    fr.close()
    fn.close()


def main():
    outp = mystem_go()
    make_ins(outp)

if __name__ == '__main__':
    main()