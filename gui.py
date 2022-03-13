import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfilename
import os, main


def select_apt_path():
    path_ = askopenfile()
    if path_:
        apt_path.set(path_.name.replace('/', '\\'))
        pch_default_path = r'D:\liubaishuo\liubs\macros\VTX550_post_processor' +'\\'

        pch_path.set(pch_default_path + apt_path.get()[apt_path.get().rfind('\\') + 1 : apt_path.get().rfind('.')] + '.pch')
        #print(path.get())
        #apt_path_entry.delete(0, tk.END)
        #apt_path_entry.insert(0, path.get())

def select_pch_path():
    path_ = asksaveasfilename()
    #print(path_)
    if path_:
        pch_path.set(path_.replace('/', '\\'))


def exec_main(apt_file_path, pch_file_path):
    main.main(apt_file_path, pch_file_path)
    print('Done!')



#===================main====================
#===================main====================
#===================main====================



root  = tk.Tk()

root.title('VTX550 post processor')


root.geometry('700x300')
root.resizable(width=False, height=False)

apt_path = tk.StringVar()
pch_path = tk.StringVar()

apt_path_entry = tk.Entry(root, textvariable = apt_path, width= 90)
apt_path_entry.grid(row=0, column=0)

select_apt_path_button = tk.Button(root , text = 'select apt file', command = select_apt_path)
select_apt_path_button.grid(row=1, column=0)

pch_path_entry = tk.Entry(root, textvariable = pch_path, width= 90)
pch_path_entry.grid(row=3, column=0)

select_pch_path_button = tk.Button(root , text = 'select pch file', command = select_pch_path)
select_pch_path_button.grid(row=4, column=0)


exec_main_button = tk.Button(root , text = 'execute', command = lambda : exec_main(apt_path.get(), pch_path.get()))
exec_main_button.grid(row=6, column=0)



root.mainloop()
