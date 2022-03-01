







'''
===========================main==============================
===========================main==============================
===========================main==============================
'''
import read_apt_file, op
import datetime

apt_txt = read_apt_file.txt_temp

pch_txt = op.main(apt_txt)

program_number = read_apt_file.apt_filename
filename_out = 'CVZ' + program_number + '.pch'

pch_txt.insert(0, 'O' + program_number[-4:])
pch_txt.insert(0, '%')
dt = datetime.datetime.now()
time_str = '(CVZ{}  '.format(program_number) + dt.strftime('%a  %b-%d-%Y  %H:%M:%S') + ')'
pch_txt.insert(2, time_str)



file_out = open(filename_out, mode='w', encoding='utf-8')
for i in pch_txt:
    file_out.write(i + '\n')
file_out.close
