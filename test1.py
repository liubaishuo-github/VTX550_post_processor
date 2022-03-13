def a():
    global ss
    print(ss)

def b():
    ss = 30
    a()


b()
