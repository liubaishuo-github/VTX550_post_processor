import os, re

def txt_connect(txt_before):
    #connect the lines divided by $, and put into txt
    txt = []
    temp = ''
    for i in txt_before:
        i = i.strip('\n')
        if i == '':
            continue
        if i[-1] != '$':
            txt.append((temp + i).strip('\n'))
            temp = ''
        else:
            temp = temp + i.rstrip('$')
    return txt


def main(apt_file_path):

    cvz_number = re.search('\d+', apt_file_path[apt_file_path.rfind('\\'):]).group()

    dir = os.getcwd()

    with open(apt_file_path, encoding='utf-8-sig') as file:
        txt_temp = file.readlines()


    txt_temp = txt_connect(txt_temp)

    return txt_temp, cvz_number
#print(txt_temp)
