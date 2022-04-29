import read_apt_file, op
import datetime, re, os

def main(apt_file_path, pch_file_path):
    #print('apt_file_path in main:', apt_file_path)
    temp = read_apt_file.main(apt_file_path)
    apt_txt = temp[0]
    cvz_number = temp[1]


    pch_txt = op.main(apt_txt)




    pch_txt.insert(0, 'O1' + cvz_number[-3:])
    pch_txt.insert(0, '%')
    dt = datetime.datetime.now()
    time_str = '(CVZ{}  '.format(cvz_number) + dt.strftime('%a  %b-%d-%Y  %H:%M:%S').upper() + ')'
    pch_txt.insert(2, time_str)



    with open(pch_file_path, mode='w', encoding='utf-8') as file_out:
        for i in pch_txt:
            file_out.write(i + '\n')

    print('==================Done======================')




if __name__ == '__main__':
    print('==========================')
    print('VTX550 post processor.')
    print('--------------------------')
    apt_filename = re.search('\d+', input("Input the apt file #:").strip()).group()

    dir = os.getcwd()

    apt_file_path = rf"{dir}\\CVZ{apt_filename}.aptsource"

    main(apt_file_path)
