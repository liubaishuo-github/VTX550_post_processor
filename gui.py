import tkinter as tk
from tkinter.filedialog import askopenfile
import os
#初始化Tk()

def selectPath():
    path_ = askopenfile()
    if path_:
        path.set(path_.name.replace('/', '\\'))
        print(path.get())
        e.delete(0, tk.END)
        e.insert(0, path.get())


root  = tk.Tk()
#设置标题
root.title('VTX550 post processor')
#设置窗口大小
width = 600
height = 300
#获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
root.geometry(alignstr)
#设置窗口是否可变长、宽，True：可变，False：不可变
root.resizable(width=False, height=False)
#进入消息循环
path = tk.StringVar()
#path.set(os.path.abspath('.'))

e = tk.Entry(root, width= 80)
e.grid()

ss = tk.Button(root , text = 'select apt file', command = selectPath)
ss.grid()

root.mainloop()
