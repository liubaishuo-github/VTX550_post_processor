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


import os, re

print('==========================')
print('VTX550 post processor.')
print('--------------------------')
apt_filename = re.search('\d+', input("Input the apt file #:").strip()).group()

dir = os.getcwd()

filename = rf"{dir}\\CVZ{apt_filename}.aptsource"

file = open(filename, encoding='utf-8-sig')
txt_temp = file.readlines()
file.close

txt_temp = txt_connect(txt_temp)
#print(txt_temp)
