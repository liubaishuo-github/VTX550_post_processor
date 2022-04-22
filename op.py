import re, copy, math, os

class Point():
    def __init__(self):
        self.x , self.y, self.z = 99.0, 99.0, 99.0
class Normal():
    def __init__(self):
        self.i, self.j, self.k = 0.0, 0.0, 0.0
class Angle():
    def __init__(self):
        self.b, self.c = 9999.0, initial_c
class Apt_point():
    def __init__(self):
        self.point = Point()
        self.normal = Normal()
        self.ball_center_point = Point()
    def extract_point_and_normal(self, apt_txt):
        temp = re.findall('-?\d+\.\d+', apt_txt)
        self.point.x, self.point.y, self.point.z, \
            self.normal.i, self.normal.j, self.normal.k= \
            list(map(float,temp))
        self.ball_center_point.x = self.point.x + float(cutting_tool_collection[tool_number].radius) * self.normal.i
        self.ball_center_point.y = self.point.y + float(cutting_tool_collection[tool_number].radius) * self.normal.j
        self.ball_center_point.z = self.point.z + float(cutting_tool_collection[tool_number].radius) * self.normal.k

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
            b_str = 'A' + str(self.angle.b)
        if self.angle.c == last_pch_point.angle.c:
            c_str = ''
        else:
            c_str = 'C[' + str(self.angle.c) + '+#5]'
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

class Cutting_Tool():
    def __init__(self, pocket, lib_number):
        dir = r'G:\IMSpost\Tooldata\SPWAEC_VTX550'
        if not(os.path.exists(dir)):
            print('!! Tooldata not exist !!')
            dir = os.getcwd()
        with open(rf'{dir}\SPWAEC_VTX550', encoding='utf-8-sig') as file:
            lines = file.readlines()
            for i in lines:
                if re.match(lib_number, i.strip()):
                    data = i.strip().split(',')
                    break
        self.pocket = pocket
        self.lib_number = lib_number
        self.assembly = data[1].strip()
        self.cutter = data[2].strip()
        self.holder = data[3].strip()
        self.adapter = data[4].strip()
        self.description = data[5].strip()
        self.gauge_length = float(data[6].strip())
        self.clearance = data[7].strip()
        self.diameter = data[8].strip()
        self.radius = data[9].strip()

def initial_g_code_status():
    global status_should_be, status_under_last

    status_should_be =  {'G90':1, 'G54':1, 'G0':0, 'G1':0, 'G43':1, 'G94':1, 'G93':0, 'F':0, 'H':1}
    status_under_last = {'G90':0, 'G54':0, 'G0':1, 'G1':0, 'G43':0, 'G94':0, 'G93':0, 'F':0, 'H':0}

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
        def rot_z(de):
            t = mat([
                      [ cos(de), -sin(de), 0, 0],
                      [ sin(de),  cos(de), 0, 0],
                      [       0,        0, 1, 0],
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
        if apt_point.normal.i != 0 or apt_point.normal.j != 0:
            c_pending1 = atan2(-apt_point.normal.i, apt_point.normal.j)
        else:
            print('caution,j,k = 0!')
            if last_pch_point.angle.c == initial_c:
                last_pch_point.angle.c = 0.
                c_pending1 = radians(last_pch_point.angle.c)
            else:
                c_pending1 = radians(last_pch_point.angle.c)

        b_pending1 = atan2(apt_point.normal.j, -apt_point.normal.k * cos(c_pending1))

        c_pending2 = c_pending1 + pi
        b_pending2 = -b_pending1
        #print('for bug:',last_pch_point.angle.__dict__)
        #print('c_pending1=',c_pending1)
        #print('c_pending2=',c_pending2)
        if cos(c_pending1 - radians(last_pch_point.angle.c)) >= cos(c_pending2 - radians(last_pch_point.angle.c)):
            c, b = nearest_c(c_pending1), b_pending1
        else:
            c, b = nearest_c(c_pending2), b_pending2
        pch_xyz = translation_z(-450/25.4) * rot_x(-b) * translation_z(-100/25.4) * rot_z(-c) * apt_plus_gl_point
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
    status_under_last['F'] = 0
    status_should_be['G1'] = 1
    status_should_be['G0'] = 0
    return 0, ''
def RAPID(apt_str):
    global status_should_be
    status_should_be['F'] = 0
    status_should_be['G0'] = 1
    status_should_be['G1'] = 0
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
def PPRINT(apt):
    temp = apt[7:].strip()
    temp = temp.replace('(', '')
    temp = temp.replace(')', '')
    temp = temp.replace('/', '')
    a = '(' + temp + ')'
    return 1, a
def LOADTL(apt_str):
    global tool_number, feedrate, last_pch_point, last_apt_point, gl
    tool_number = re.search('\d+', apt_str).group()
    gl = cutting_tool_collection[tool_number].gauge_length
    feedrate = -999
    initial_g_code_status()

    last_pch_point = Pch_point()
    last_apt_point = Apt_point()

    loadtool_head1 = ['G53G0G49Z0.', 'M9', 'M5', 'G54.3P0','G92.1X0.Y0.Z0.A0.C0.',
                    '(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)',
                    '(LOAD TOOL NO: {}   {} )'.format(tool_number, cutting_tool_collection[tool_number].cutter),
                    '(TOOL GL: {}   TOOL RADIUS: {} )'.format(gl, cutting_tool_collection[tool_number].radius),
                    '(* * * * * * * * * * * * * * * * * * * * * * * * * * * * * *)',
                    'M1']
    output_str =[]
    for i in loadtool_head1:
        output_str.append(i)

    n_number_of_if = print_N_number()
    n_number = int(re.search('\d+', n_number_of_if).group())
    output_str.append(n_number_of_if + 'IF[#599EQ{}]GOTO{} (RESTART)'.format(tool_number, str(n_number +3)))
    if fixture_offset_comp:
        foc_str = 'G54.3P1'
    else:
        foc_str = ''

    loadtool_end1 = ['T' + tool_number,
					 'M6', 'G53G49Z0.',
					 'G54.3P0',
					 'G92.1X0.Y0.Z0.A0.C0.',
					 'G90G54G0C' + str(initial_c),
					 foc_str,
					 ]
    for i in loadtool_end1:
        output_str.append(print_N_number() + i)

    return 2, output_str
def SPINDL(apt):
    if re.search('OFF',apt):
        a = 'M5'
        return 1, print_N_number() + a

    rpm = re.search('\d+', apt).group()
    if re.search('CLW', apt) and not(re.search('CCLW', apt)):
        dir = 'M3'
    elif re.search('CCLW', apt):
        dir = 'M4'

    a = '{}S{}'.format(dir, rpm)
    return 1, print_N_number() + a
def AICC(apt):
    if re.search('OFF',apt):
        a = 'G05.1Q0'
        return 1, a
    if re.search('\d+', apt):
        level = re.search('\d+', apt).group()
    else:
        level = '1'
    a = 'G05.1Q1R{}'.format(level)
    return 1, a
def TOOLNO(apt):
    global cutting_tool_collection
    tool_pocket = re.search('\d+', apt[:apt.find(',')]).group()
    #print(apt)
    tool_lib_number = re.search('(\d+\.?\d+|\d+)', apt[apt.find(',')+1 :]).group()
    tool_instance = Cutting_Tool(tool_pocket, tool_lib_number)
    cutting_tool_collection[tool_pocket] = tool_instance
    tool_description = [
                        '(---------------------------------------------------------)',
                        '(POCKET #:{}                                  LIB#:{}'.format(tool_pocket, tool_lib_number).ljust(58) + ')',
                        '({}  {}  GL:{}   C/L:{}  RADIUS:{}'.format(tool_instance.cutter, tool_instance.description, tool_instance.gauge_length, tool_instance.clearance, tool_instance.radius).ljust(58) + ')',
                        '(ASSEMBLY:{}'.format(tool_instance.assembly).ljust(58) + ')',
                        '(HOLDER:{}'.format(tool_instance.holder).ljust(58) + ')',
                        '(ADAPTER:{}'.format(tool_instance.adapter).ljust(58) + ')',
                        '(---------------------------------------------------------)',
                        ]
    return 2, tool_description
def OPERATION_NAME(apt):
    temp = apt[apt.find(':') + 1 : ].strip()
    temp = temp.replace('(', '')
    temp = temp.replace(')', '')
    a = '(' + temp + ')'
    return 1, a
def STOP(apt):
    return 1, print_N_number() + 'M0'
def COOLNT(apt):
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
                    '#5=0']
        temp = print_N_number() + 'M1'
        loop_N_number_stack.append(re.search('\d+', temp).group())
        start_words.append(temp)
        start_words.append(print_N_number() + 'C[' + str(last_pch_point.angle.c) + '+#5]')
        return 2, start_words

    if re.search('END', apt):
        temp = print_N_number() + '#5=0'
        end_words = ['#5=#577*360/{}'.format(loop_number_stack.pop()),\
                    'IF[#575LE#577]GOTO{}'.format(re.search('\d+', temp).group()),\
                    '#577=#577+1', 'GOTO{}'.format(loop_N_number_stack.pop())]
        end_words.append(temp)
        end_words.append(print_N_number() + 'C' + str(last_pch_point.angle.c))
        end_words.append('(LOOP EEEEEEEEEEEEEEEEEEEEEEEEEEEEND)')
        return 2, end_words
def FIXOFTCO(apt):
    global fixture_offset_comp
    if re.search('ON',apt):
        fixture_offset_comp = True
    elif re.search('OFF',apt):
        fixture_offset_comp = False
    return 0, ''



def add_program_head():
    global pch_txt
    program_head = ['G90G20G17G54G64', 'G80', 'G40', 'M25', 'M5', 'M9', '#5205=0', '#5=0', '#580=0.1']
    for i in program_head:
        pch_txt.append(i)

def add_program_end():
    global pch_txt
    program_end = ['M9', 'M5', 'G0G90G53G49Z.0', 'G80G40', 'X.0Y.0Z.0A.0C.0', 'G54.3P0', 'T0', 'M6', 'M26', 'M30']
    for i in program_end:
        pch_txt.append(print_N_number() + i)
    pch_txt.append('%')


def main(apt_txt):
    global pch_txt, loop_N_number_stack, loop_number_stack, cutting_tool_collection, last_pch_point, last_apt_point
    global block_number, gl, tool_number, feedrate, initial_c, fixture_offset_comp
    #print(';=====')
    #print(last_pch_point.angle.c)
    initial_c = 0.
    pch_txt = []
    loop_N_number_stack = []
    loop_number_stack = []
    cutting_tool_collection = {}
    last_pch_point = Pch_point()
    last_apt_point = Apt_point()

    block_number = 0
    gl = 9.999
    tool_number = 0
    feedrate = -999
    fixture_offset_comp = True

    initial_g_code_status()

    ppword_list = {
                    'GOTO':'GOTO',
                    'RAPID':'RAPID',
                    'INVERSE':'INVERSE',
                    'FEDRAT':'FEDRAT',
                    'STOP':'STOP',
                    'SPINDL':'SPINDL',
                    'LOADTL':'LOADTL',
                    'COOLNT':'COOLNT',
                    'LOOP':'LOOP',
                    '\$\$ OPERATION NAME :':'OPERATION_NAME',
                    'TOOLNO':'TOOLNO',
                    'AICC':'AICC',
                    'PPRINT':'PPRINT',
                    'FIXOFTCO':'FIXOFTCO'
                    }

    add_program_head()

    for i in apt_txt:
        #print(i)
        for key, value in ppword_list.items():
            ppword_match_object = re.match(key,i)
            if ppword_match_object:
                #print("match success:" + i)
                lc = locals()
                exec('temp =' + value + '(i)')
                temp = lc['temp']
                #print(temp)
                if temp[0] == 1:
                    pch_txt.append(temp[1])
                elif temp[0] ==2:
                    pch_txt.extend(temp[1])
                break

    add_program_end()

    #for i in pch_txt:
    #    print(i)
    return pch_txt
