#global block_number, gl, last_pch_point, last_apt_point, feedrate
block_number = 0
gl = 9.999
tool_number = 0
feedrate = -999
status_g94_g93_stack = []
status_should_be =  {'G90':1, 'G54':1, 'G0':0, 'G1':1, 'G43':1, 'G94':1, 'G93':0, 'F':0, 'H':1}
status_under_last = {'G90':0, 'G54':0, 'G0':0, 'G1':0, 'G43':0, 'G94':0, 'G93':0, 'F':0, 'H':0}


import re, copy, math

class Point():
    def __init__(self):
        self.x , self.y, self.z = 99.0, 99.0, 99.0
class Normal():
    def __init__(self):
        self.i, self.j, self.k = 0.0, 0.0, 0.0
class Angle():
    def __init__(self):
        self.b, self.c = 9999.0, 0.0
class Apt_point():
    def __init__(self):
        self.point = Point()
        self.normal = Normal()
    def extract_point_and_normal(self, apt_txt):
        temp = re.findall('-?\d+\.\d+', apt_txt)
        self.point.x, self.point.y, self.point.z, \
            self.normal.i, self.normal.j, self.normal.k= \
            list(map(float,temp))
class Pch_point():
    def __init__(self):
        self.point = Point()
        self.angle = Angle()
    @staticmethod
    def print_feedrate():
        if status_should_be['G94'] == 1:
            return str(feedrate)
        elif status_should_be['G93'] == 1:
            #print(current_apt_point.point.__dict__)
            #print(last_apt_point.point.__dict__)
            distance = math.sqrt(math.pow(current_apt_point.point.x - last_apt_point.point.x, 2) + \
                                math.pow(current_apt_point.point.y - last_apt_point.point.y, 2) + \
                                math.pow(current_apt_point.point.z - last_apt_point.point.z, 2))
            inverse_feedrate = min(round(feedrate / distance, 3), 99999.999)
            return str(inverse_feedrate)
    def print_point(self):
        if self.point.x == last_pch_point.point.x:
            x_str = ''
        else:
            x_str = 'X' + str(self.point.x)
        if self.point.y == last_pch_point.point.y:
            y_str = ''
        else:
            y_str = 'Y' + str(self.point.y)
        if self.point.z == last_pch_point.point.z:
            z_str = ''
        else:
            z_str = 'Z' + str(self.point.z)
        if self.angle.b == last_pch_point.angle.b:
            b_str = ''
        else:
            b_str = 'B' + str(self.angle.b)
        if self.angle.c == last_pch_point.angle.c and self.angle.c != 0:
            c_str = ''
            '''This is to avoid the first point'C is just 0'''
        else:
            c_str = 'C' + str(self.angle.c)
        return x_str + y_str + z_str + b_str + c_str
    def print_g_code(self):
        global status_under_last
        g_code_str = ''
        f_h_str = ''
        for key in status_should_be.keys():
            if status_should_be[key] == 1 and status_under_last[key] == 0:
                if key != 'F' or status_should_be['G93'] == 0:
                    status_under_last[key] = 1
                if key == 'F':
                    f_h_str += 'F' + self.print_feedrate()
                elif key == 'H':
                    f_h_str += key + str(tool_number)
                else:
                    g_code_str += key

        return g_code_str, f_h_str

def updata_g_code_status():
    def clear_status(if_one, to_be_zero):
        global status_under_last
        if status_should_be[if_one] == 1:
            status_under_last[to_be_zero] = 0
        if status_should_be[to_be_zero] == 1:
            status_under_last[if_one] =0
    clear_status('G0', 'G1')
    clear_status('G94', 'G93')
    status_should_be['G0'] = 0
    status_should_be['G1'] = 1
    #if status_g94_g93_stack != []:
    #    status_should_be[status_g94_g93_stack.pop()] = 1
    if status_should_be['G93'] ==1:
        status_should_be['F'] = 1

def print_N_number():
    global block_number
    block_number += 1
    return 'N' + str(block_number)

def GOTO(apt_str):
    global last_apt_point, last_pch_point, current_apt_point
    def transf(apt_point):
        from numpy import mat
        from math import sin, cos, radians, degrees, \
                        radians, asin, atan2, fabs, pi

        def translation_z(dis):
            t = mat([
                        [ 1, 0, 0, 0],
                        [ 0, 1, 0, 0],
                        [ 0, 0, 1, dis],
                        [ 0, 0, 0, 1],
                                        ])
            return t
        def translation_x(dis):
            t = mat([
                        [ 1, 0, 0, dis],
                        [ 0, 1, 0, 0],
                        [ 0, 0, 1, 0],
                        [ 0, 0, 0, 1],
                                        ])
            return t
        def rot_y(de):
            t = mat([
                        [ cos(de), 0, sin(de), 0],
                        [ 0,       1,       0, 0],
                        [-sin(de), 0, cos(de), 0],
                        [0, 0, 0, 1]
                                                    ])
            return t
        def rot_x(de):
            t = mat([
                        [1, 0, 0, 0],
                        [0, cos(de), -sin(de), 0],
                        [0, sin(de), cos(de), 0],
                        [0, 0, 0, 1]
                                                    ])
            return t
        def nearest_c(de):
            ''' de is in radians '''
            nearest_c = de
            c = radians(last_pch_point.angle.c)
            target = c - de
            if target == 0:
                return de
            if c - de > 0:
                sign = 1
            else:
                sign = -1
            delta = 2 * pi * sign
            temp = de
            while fabs(temp - c) > pi:
                temp = temp + delta
            return temp

        apt_plus_gl_point = mat([apt_point.point.x + apt_point.normal.i * gl,\
                                apt_point.point.y + apt_point.normal.j * gl,\
                                apt_point.point.z + apt_point.normal.k * gl,\
                                1]).T
        if apt_point.normal.j != 0 or apt_point.normal.k != 0:
            c_pending1 = atan2(apt_point.normal.j, apt_point.normal.k)
        else:
            c_pending1 = radians(last_pch_point.angle.c)
            print('caution,j,k = 0!')
        b_pending1 = atan2(apt_point.normal.i,
                            apt_point.normal.j * sin(c_pending1) + \
                            apt_point.normal.k * cos(c_pending1))
        c_pending2 = c_pending1 + pi
        b_pending2 = pi - b_pending1
        #print('for bug:',last_pch_point.angle.__dict__)
        #print('c_pending1=',c_pending1)
        #print('c_pending2=',c_pending2)
        if cos(c_pending1 - radians(last_pch_point.angle.c)) >= cos(c_pending2 - radians(last_pch_point.angle.c)):
            c, b = nearest_c(c_pending1), b_pending1
        else:
            c, b = nearest_c(c_pending2), b_pending2
        pch_xyz = translation_z(-37.3964) * rot_y(-b) * rot_x(c) *translation_x(3) * apt_plus_gl_point
        x, y, z = pch_xyz[0,0], pch_xyz[1,0], pch_xyz[2,0]
        return round(x,4), round(y,4), round(z,4), round(degrees(b),3), round(degrees(c),3)

    current_apt_point = Apt_point()
    current_apt_point.extract_point_and_normal(apt_str)

    current_pch_point = Pch_point()

    current_pch_point.point.x, current_pch_point.point.y, current_pch_point.point.z\
    ,current_pch_point.angle.b,current_pch_point.angle.c = transf(current_apt_point)

    temp = current_pch_point.print_g_code()

    output_str = print_N_number() + temp[0] + current_pch_point.print_point() + temp[1]

    updata_g_code_status()

    last_apt_point = current_apt_point
    last_pch_point = current_pch_point

    return 1, output_str
def FEDRAT(apt_str):
    global feedrate, status_should_be, status_under_last
    feedrate = round(float(re.findall('\d+\.\d+', apt_str)[0]),3)
    status_should_be['F'] = 1
    status_should_be['G1'] = 1
    status_should_be['G0'] = 0
    status_under_last['F'] = 0
    return 0, ''
def RAPID(apt_str):
    global status_should_be, status_g94_g93_stack
    status_should_be['F'] = 0
    status_should_be['G0'] = 1
    status_should_be['G1'] = 0
    if status_should_be['G93'] == 1:
        status_g94_g93_stack.append('G93')
    elif status_should_be['G94'] == 1:
        status_g94_g93_stack.append('G94')
    #status_should_be['G93'] = 0
    #status_should_be['G94'] = 0
    return 0, ''
def INVERSE(apt_str):
    global status_should_be
    if re.search('ON',apt_str):
        status_should_be['G93'] = 1
        status_should_be['G94'] = 0
    elif re.search('OFF',apt_str):
        status_should_be['G93'] = 0
        status_should_be['G94'] = 1
    return 0, ''
def LOADTOOL(apt_str):
    global tool_number, feedrate, status_g94_g93_stack, status_should_be, status_under_last, last_pch_point, last_apt_point, gl
    tool_number = re.search('(\d+)( *),( *)(\d+\.\d+|\d+|\.\d+)', apt_str).group(1)
    gl =    float(re.search('(\d+)( *),( *)(\d+\.\d+|\d+|\.\d+)', apt_str).group(4))
    feedrate = -999
    status_g94_g93_stack = []
    status_should_be =  {'G90':1, 'G54':1, 'G0':0, 'G1':1, 'G43':1, 'G94':1, 'G93':0, 'F':0, 'H':1}
    status_under_last = {'G90':0, 'G54':0, 'G0':0, 'G1':0, 'G43':0, 'G94':0, 'G93':0, 'F':0, 'H':0}
    last_pch_point = Pch_point()
    last_apt_point = Apt_point()

    loadtool_head1 = ['G0G49Z0', 'M5', '(******************************)',\
                    '(LOAD TOOL #{} , GL={} )'.format(tool_number, gl),\
                    '(******************************)', 'M1']
    output_str =[]
    for i in loadtool_head1:
        output_str.append(print_N_number() + i)

    n_number_of_if = print_N_number()
    n_number = int(re.search('\d+', n_number_of_if).group())
    output_str.append(n_number_of_if + 'IF[#599EQ{}]GOTO{} (RESTART)'.format(tool_number, str(n_number +3)))

    output_str.extend([print_N_number() + 'T' + tool_number, print_N_number() + 'M6'])

    return 2, output_str
def SPINDLE(apt):
    if re.search('STOP',apt):
        a = 'M5'
        return 1, print_N_number() + a

    rpm = re.search('\d+', apt).group()
    if re.search('CLW', apt) and not(re.search('CCLW', apt)):
        dir = 'M3'
    elif re.search('CCLW', apt):
        dir = 'M4'

    a = '{}S{}'.format(dir, rpm)
    return 1, print_N_number() + a
def STOP(apt):
    return 1, print_N_number() + 'M0'
def SHUI(apt):
    if re.search('ON',apt):
        a = 'M20'
        return 1, '/2' + print_N_number() + a
    if re.search('OFF', apt):
        a = 'M9'
        return 1, print_N_number() + a
def LOOP(apt):
    global loop_N_number_stack, loop_number_stack
    if re.search('START', apt):
        loop_number_stack.append(re.search('\d+', apt).group())
        loop_number_stack.append(re.search('\d+', apt).group())
        start_words = ['(LOOP SSSSSSSSSSSSSSSSSSSSSSSSSTART)', \
                    '#575={} (#575 is total loop number)'.format(loop_number_stack.pop()),\
                    '#576=0 (#576 is initial number)',\
                    '#577=#576+1 (#577 is current loop number)', \
                    '#5205=0 (#5205 is C axis external)']
        temp = print_N_number() + 'M1'
        loop_N_number_stack.append(re.search('\d+', temp).group())
        start_words.append(temp)
        start_words.append(print_N_number() + 'C' + str(last_pch_point.angle.c))
        return 2, start_words

    if re.search('END', apt):
        temp = print_N_number() + '#5205=0'
        end_words = ['#5205=#577*360/{}'.format(loop_number_stack.pop()),\
                    'IF[#575LE#577]GOTO{}'.format(re.search('\d+', temp).group()),\
                    '#577=#577+1', 'GOTO{}'.format(loop_N_number_stack.pop())]
        end_words.append(temp)
        end_words.append(print_N_number() + 'C' + str(last_pch_point.angle.c))
        end_words.append('(LOOP EEEEEEEEEEEEEEEEEEEEEEEEEEEEND)')
        return 2, end_words


def add_program_head():
    global pch_txt
    program_head = ['G90G20G17G54G64', 'M25', '#5205=0']
    for i in program_head:
        pch_txt.append(i)

def add_program_end():
    global pch_txt
    program_end = ['M9', 'M5', 'G0G90G49Z.0', 'X.0Y.0Z.0B.0C.0', 'T0', 'M6', 'M26', 'M30']
    for i in program_end:
        pch_txt.append(print_N_number() + i)
    pch_txt.append('%')


def main(apt_txt):
    global pch_txt
    #print(';=====')
    #print(last_pch_point.angle.c)
    ppword_list = ['GOTO', 'RAPID', 'INVERSE', 'FEDRAT', 'STOP',\
                    'SPINDLE', 'LOADTOOL', 'SHUI', 'LOOP']

    add_program_head()

    for i in apt_txt:
        for j in ppword_list:
            ppword_match_object = re.match(j,i)
            if ppword_match_object:
                ppword = ppword_match_object.group()
                #print("match success:" + i)
                lc = locals()
                exec('temp =' + ppword + '(i)')
                temp = lc['temp']
                #print(temp)
                if temp[0] == 1:
                    pch_txt.append(temp[1])
                elif temp[0] ==2:
                    pch_txt.extend(temp[1])
                break

    add_program_end()

    for i in pch_txt:
        print(i)
    return pch_txt

#==================main==================================
pch_txt = []
loop_N_number_stack = []
loop_number_stack = []
last_pch_point = Pch_point()
last_apt_point = Apt_point()
