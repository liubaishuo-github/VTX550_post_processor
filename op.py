import re, copy, math, os
from numpy import mat, cross
from math import sin, cos, radians, degrees, asin, atan2, fabs, pi

class Point():
    def __init__(self):
        self.x , self.y, self.z = 99.0, 99.0, -99.0
class Canned_cycle_point():
    def __init__(self):
        dwell = None
        inter_feed = None
        lift_dis = None
        if canned_cycle_para['dwell'] != None:
            dwell = int(canned_cycle_para['dwell'] * 1000)
        if canned_cycle_para['inter_feed'] != None:
            inter_feed = round(canned_cycle_para['inter_feed'], 4)
        if canned_cycle_para['lift_dis'] != None:
            lift_dis = round(canned_cycle_para['lift_dis'], 4)

        self.g73 = {'R':None, 'Q':inter_feed}
        self.g74 = {'R':None, 'P':dwell}
        self.g76 = {'R':None, 'Q':lift_dis, 'P':dwell}
        self.g81 = {'R':None}
        self.g82 = {'R':None, 'P':dwell}
        self.g83 = {'R':None, 'Q':inter_feed}
        self.g84 = {'R':None, 'P':dwell}
        self.g85 = {'R':None}
        self.g86 = {'R':None}
        #self.g87 = {'R':None, 'Q':lift_dis, 'P':dwell}
        #self.g88 = {'R':None, 'P':dwell}
        self.g89 = {'R':None, 'P':dwell}
class Circular_point():
    def __init__(self):
        self.i, self.j, self.k = None, None, None

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
        self.canned_cycle = Canned_cycle_point()
        self.circular_point = Circular_point()
    @staticmethod
    def f(a):
        if float(a) == 0:
            return '0.'
        if float(a) > 0:
            return a.lstrip('0')
        if float(a) < 0:
            return a.replace('-0', '-')
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
            x_str = 'X' + self.f(str(self.point.x))
        if self.point.y == last_pch_point.point.y:
            y_str = ''
        else:
            y_str = 'Y' + self.f(str(self.point.y))
        if self.point.z == last_pch_point.point.z:
            z_str = ''
        else:
            z_str = 'Z' + self.f(str(self.point.z))
        if self.angle.b == last_pch_point.angle.b:
            b_str = ''
        else:
            b_str = 'A' + self.f(str(self.angle.b))
        if self.angle.c == last_pch_point.angle.c:
            c_str = ''
        else:
            if len(loop_number_stack) > 0:
                c_str = 'C[' + self.f(str(self.angle.c)) + '+#5]'
            else:
                c_str = 'C' + self.f(str(self.angle.c))
        return x_str + y_str + z_str + b_str + c_str
    def print_canned_cycle_point(self): #print R Q P etc...

        if status_should_be['CYCLE'] != 1:
            return ''

        temp_str = ''

        temp_dict = getattr(self.canned_cycle, current_cycle_gcode())

        for key in temp_dict.keys():
            if temp_dict[key] != getattr(last_pch_point.canned_cycle, current_cycle_gcode())[key]:
                if key != 'P':  # P(dwell time) must not contain decimal point
                    temp_str += key + self.f(str(temp_dict[key]))
                else:
                    temp_str += key + str(temp_dict[key])


        return temp_str
    def print_circular_point(self):
        return 'I' + self.f(str(self.circular_point.i)) + 'J' + self.f(str(self.circular_point.j))
    @staticmethod
    def print_cycle_code():
        temp = 'G98'
        for key in status_should_be_cycle.keys():
            if status_should_be_cycle[key] == 1 and status_under_last_cycle[key] == 0:
                status_under_last_cycle[key] = 1
                temp += key
        return temp
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
                elif key != 'CYCLE':
                    g_code_str += key
                elif key == 'CYCLE':
                    g_code_str += self.print_cycle_code()

        return g_code_str, f_h_str

class Cutting_Tool():
    def __init__(self, pocket, lib_number):
        dir = r'G:\IMSpost\Tooldata'
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
    global status_should_be, status_under_last, status_should_be_cycle, status_under_last_cycle

    status_should_be =  {'G90':1, 'G54':1, 'G0':0, 'G1':0, 'G2':0, 'G3':0, 'G43':1, 'G94':1, 'G93':0, 'F':0, 'H':1, 'CYCLE':0}
    status_under_last = {'G90':0, 'G54':0, 'G0':1, 'G1':0, 'G2':0, 'G3':0, 'G43':0, 'G94':0, 'G93':0, 'F':0, 'H':0, 'CYCLE':0}
    #status_under_last of 'G0':1 , because of setting G0C0.0 after every LOADTL
    status_should_be_cycle =  {'G73':0, 'G74':0, 'G76':0, 'G81':0, 'G82':0, 'G83':0, 'G84':0, 'G85':0, 'G86':0, 'G87':0, 'G88':0, 'G89':0, }
    status_under_last_cycle = {'G73':0, 'G74':0, 'G76':0, 'G81':0, 'G82':0, 'G83':0, 'G84':0, 'G85':0, 'G86':0, 'G87':0, 'G88':0, 'G89':0, }

def updata_g_code_status():
    def clear_status_in_fanuc(clear_list):
        global status_under_last
        for i in clear_list:
            if status_should_be[i] == 1:
                for j in clear_list:
                    if j != i:
                        status_under_last[j] = 0
                break


    clear_status_in_fanuc(['G0', 'G1', 'CYCLE', 'G2', 'G3'])
    clear_status_in_fanuc(['G94', 'G93'])


    if status_under_last['CYCLE'] == 0:
        status_should_be['G1'] = 1

    if status_should_be['G93'] ==1:
        status_should_be['F'] = 1
        status_under_last['F'] = 0

def current_cycle_gcode():
    for key in status_should_be_cycle.keys():
        if status_should_be_cycle[key] == 1:
            return key.lower()
def print_N_number():
    global block_number
    block_number += 1
    return 'N' + str(block_number)
def overtravel_check(apt_str, pch_str):
    assert (last_pch_point.point.z is None) or (last_pch_point.point.z <= 0),\
        '+Z OVER TRAVEL at:\n{}\n it will be:\n{}'.format(apt_str, pch_str)

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

def transf(apt_point):

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
        c_pending1 = -atan2(apt_point.normal.i, apt_point.normal.j)
    else:
        print('caution,j,k = 0!')
        if last_pch_point.angle.c == initial_c:
            last_pch_point.angle.c = 0.
            c_pending1 = radians(last_pch_point.angle.c)
        else:
            c_pending1 = radians(last_pch_point.angle.c)

    b_pending1 = -atan2(sin(-c_pending1)*apt_point.normal.i + cos(-c_pending1)*apt_point.normal.j, apt_point.normal.k)

    c_pending2 = c_pending1 + pi
    b_pending2 = -b_pending1
    #print(degrees(c_pending1),'  ', degrees(c_pending2))
    #print(degrees(b_pending1),'  ', degrees(b_pending2))
    if cos(c_pending1 - radians(last_pch_point.angle.c)) >= cos(c_pending2 - radians(last_pch_point.angle.c)):
        c, b = nearest_c(c_pending1), b_pending1
    else:
        c, b = nearest_c(c_pending2), b_pending2
    pch_xyz = translation_z(-450/25.4) * rot_x(-b) * translation_z(-100/25.4) * rot_z(-c) * apt_plus_gl_point
    x, y, z = pch_xyz[0,0], pch_xyz[1,0], pch_xyz[2,0]
    return round(x, linear_decimal_digits),\
            round(y, linear_decimal_digits),\
            round(z, linear_decimal_digits),\
            round(degrees(b), angular_decimal_digits),\
            round(degrees(c), angular_decimal_digits)

def transf_circular_vector(vector):
    vector.append(1)
    temp = rot_x(radians(-last_pch_point.angle.b)) * rot_z(radians(-last_pch_point.angle.c)) * mat(vector).T
    return temp

def transf_circular_point(point):

    apt_plus_gl_point = mat([point[0] + last_apt_point.normal.i * gl,\
                            point[1] + last_apt_point.normal.j * gl,\
                            point[2] + last_apt_point.normal.k * gl,\
                            1]).T
    temp = translation_z(-450/25.4) * rot_x(radians(-last_pch_point.angle.b)) \
            * translation_z(-100/25.4) * rot_z(radians(-last_pch_point.angle.c)) \
            * apt_plus_gl_point
    return temp


def GOTO(apt_str):
    global last_apt_point, last_pch_point, current_apt_point


    current_apt_point = Apt_point()
    current_apt_point.extract_point_and_normal(apt_str)

    current_pch_point = Pch_point()

    current_pch_point.point.x, current_pch_point.point.y, current_pch_point.point.z\
    ,current_pch_point.angle.b,current_pch_point.angle.c = transf(current_apt_point)

    if status_should_be['CYCLE'] == 1:
        temp_dict = getattr(current_pch_point.canned_cycle, current_cycle_gcode())
        temp_dict['R'] = round(current_pch_point.point.z + canned_cycle_para['clear_tip'], linear_decimal_digits)

        setattr(current_pch_point.canned_cycle, current_cycle_gcode(), temp_dict)

        current_pch_point.point.z = round(current_pch_point.point.z - canned_cycle_para['total_depth'], linear_decimal_digits)

    temp = current_pch_point.print_g_code()

    output_str = print_N_number() + temp[0] + current_pch_point.print_point() + current_pch_point.print_canned_cycle_point() + temp[1]

    updata_g_code_status()
    status_should_be['G0'] = 0

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
        status_should_be['F'] = 1
        status_under_last['F'] = 0
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
    output_str.append(n_number_of_if + 'IF[#994EQ{}]GOTO{} (RESTART)'.format(tool_number, str(n_number +3)))
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
    if re.search('LOCK',apt):
        a = 'M19'
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
def CYCLE(apt):
    global status_should_be_cycle, status_under_last_cycle, feedrate, canned_cycle_para

    if re.search('OFF', apt):
        a = 'G80'
        status_should_be['CYCLE'] = 0
        status_under_last['CYCLE'] = 0
        status_should_be_cycle = dict.fromkeys(status_should_be_cycle, 0)
        status_under_last_cycle = dict.fromkeys(status_under_last_cycle, 0)
        canned_cycle_para = dict.fromkeys(canned_cycle_para, None)
        canned_cycle_para['tip_radius'] = 0
        last_pch_point.point.z = -99.0  #iniial z value after G80, to prevent accidental z issues
        return 1, print_N_number() + a
    else:
        status_should_be['F'] = 1
        status_under_last['F'] = 0
        status_should_be['CYCLE'] = 1
        status_should_be['G1'] = 0
        status_should_be['G0'] = 0

        temp = apt.split(',')

        feedrate = round(float(temp[3]),3)
        canned_cycle_para['total_depth'] = float(temp[1])
        canned_cycle_para['clear_tip'] = float(temp[5])

        if re.search('/DRILL_G81', apt):
            status_should_be_cycle['G81'] = 1
        if re.search('/DRILL_G82', apt):
            status_should_be_cycle['G82'] = 1
            canned_cycle_para['dwell'] = float(temp[7])
        if re.search('/DEEP_G83', apt):
            status_should_be_cycle['G83'] = 1
            canned_cycle_para['inter_feed'] = float(temp[7])
        if re.search('/BRKCHP_G73', apt):
            status_should_be_cycle['G73'] = 1
            canned_cycle_para['inter_feed'] = float(temp[7])
        if re.search('/TAP_G84', apt):
            status_should_be_cycle['G84'] = 1
            canned_cycle_para['dwell'] = 0.0
        if re.search('/LHTAP_G74', apt):
            status_should_be_cycle['G74'] = 1
            canned_cycle_para['dwell'] = 0.0
        if re.search('/BORE_G85', apt):
            status_should_be_cycle['G85'] = 1
            canned_cycle_para['tip_radius'] = float(temp[7])
        if re.search('/BORE_G86', apt):
            status_should_be_cycle['G86'] = 1
            canned_cycle_para['tip_radius'] = float(temp[7])
        if re.search('/BORE_G89', apt):
            status_should_be_cycle['G89'] = 1
            canned_cycle_para['dwell'] = float(temp[7])
            canned_cycle_para['tip_radius'] = float(temp[11])
        if re.search('/STPBOR_G76', apt):
            status_should_be_cycle['G76'] = 1
            canned_cycle_para['dwell'] = float(temp[7])
            canned_cycle_para['lift_dis'] = abs(float(temp[13]))
            canned_cycle_para['tip_radius'] = float(temp[15])



        return 0, ''
def STOP(apt):
    return 1, print_N_number() + 'M0'
def OPSTOP(apt):
    return 1, print_N_number() + 'M1'
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
        loop_number = re.search('\d+', apt).group()
        loop_number_stack.append(loop_number)
        start_words = [
                    '(LOOP SSSSSSSSSSSSSSSSSSSSSSSSSTART)',
                    '#575={} (#575 is total loop number)'.format(loop_number),
                    '#576=0 (#576 is initial number)',
                    '#577=#576+1 (#577 is current loop number)',
                    '#5=#576*360/{}'.format(loop_number),
					]
        temp = print_N_number() + 'M1'
        loop_N_number_stack.append(re.search('\d+', temp).group())
        start_words.append(temp)
        start_words.append(print_N_number() + 'C[' + str(last_pch_point.angle.c) + '+#5]')
        return 2, start_words

    if re.search('END', apt):
        temp = print_N_number() + '#5=0'
        loop_number = loop_number_stack.pop()
        end_words = [
					'#5=#577*360/{}'.format(loop_number),
                    'IF[#575LE#577]GOTO{}'.format(re.search('\d+', temp).group()),
                    '#577=#577+1',
					'GOTO{}'.format(loop_N_number_stack.pop()),
					]
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
def DELAY(apt):
    temp = int(float(re.search('(\d+\.?\d+|\.\d+|\d+)', apt).group()) * 1000)
    a ='G4P' + str(temp)
    return 1, print_N_number() + a
def INDIRV(apt):
    global circular_start_vector
    temp = re.findall('-?\d+\.\d+', apt)
    circular_start_vector = list(map(float, temp))
    return 0, ''
def TLON(apt):
    global last_pch_point, last_apt_point, circular_start_vector

    status_should_be['G1'] = 0

    temp = re.findall('-?\d+\.\d+', apt)[-6:]
    temp = list(map(float, temp))
    arc_center_apt = temp[0:3]
    arc_end_apt = temp[3:6]

    current_apt_point = copy.deepcopy(last_apt_point)
    current_apt_point.point.x, current_apt_point.point.y, current_apt_point.point.z = arc_end_apt[0], arc_end_apt[1], arc_end_apt[2]


    circular_start_vector_pch = transf_circular_vector(circular_start_vector)
    arc_center_pch = transf_circular_point(arc_center_apt)
    arc_start_pch = mat([last_pch_point.point.x, last_pch_point.point.y, last_pch_point.point.z, 1]).T
    vector_start_to_center = arc_center_pch - arc_start_pch
    #print(vector_start_to_center.T.tolist()[0][0:3])
    #print(circular_start_vector_pch.T.tolist()[0][0:3])
    cross_product = cross(vector_start_to_center.T.tolist()[0][0:3], circular_start_vector_pch.T.tolist()[0][0:3])
    #print(cross_product)
    if cross_product[2] > 0:
        status_should_be['G2'] = 1
    elif cross_product[2] < 0:
        status_should_be['G3'] = 1


    current_pch_point = copy.deepcopy(last_pch_point)
    temp = transf_circular_point(arc_end_apt)
    current_pch_point.point.x, current_pch_point.point.y, current_pch_point.point.z = \
                                                                        round(temp[0,0], linear_decimal_digits), \
                                                                        round(temp[1,0], linear_decimal_digits), \
                                                                        round(temp[2,0], linear_decimal_digits)

    current_pch_point.circular_point.i = round(arc_center_pch[0,0] - arc_start_pch[0,0], linear_decimal_digits)
    current_pch_point.circular_point.j = round(arc_center_pch[1,0] - arc_start_pch[1,0], linear_decimal_digits)


    temp = current_pch_point.print_g_code()
    output_str = print_N_number() + temp[0] + current_pch_point.print_point() + current_pch_point.print_circular_point() + temp[1]
    #print(current_pch_point.point.x, current_pch_point.point.y, current_pch_point.point.z, current_pch_point.angle.b, current_pch_point.angle.c)
    #print(last_pch_point.point.x, last_pch_point.point.y, last_pch_point.point.z, current_pch_point.angle.b, current_pch_point.angle.c)

    updata_g_code_status()
    status_should_be['G2'] = 0
    status_should_be['G3'] = 0

    last_apt_point = current_apt_point
    last_pch_point = current_pch_point
    return 1, output_str
def skipproc(apt):
    global skip_post_process
    if re.search('ON',apt):
        skip_post_process = True
    elif re.search('OFF',apt):
        skip_post_process = False


def add_program_head():
    global pch_txt
    program_head = ['G90G20G17G54G64', 'G80', 'G40', 'M25', 'M5', 'M9', '#5205=0.', '#5=0.', '#580=0.1']
    for i in program_head:
        pch_txt.append(i)

def add_program_end():
    global pch_txt
    program_end = ['M9', 'M5', 'G0G90G53G49Z.0', 'G80G40', 'G53X0.', 'G53Y.0Z.0A.0C.0', 'G54.3P0', 'T0', 'M6', 'M26', 'M30']
    for i in program_end:
        pch_txt.append(print_N_number() + i)
    pch_txt.append('%')


def main(apt_txt):
    global pch_txt, loop_N_number_stack, loop_number_stack, cutting_tool_collection, last_pch_point, last_apt_point
    global block_number, gl, tool_number, feedrate, initial_c, fixture_offset_comp, canned_cycle_para
    global linear_decimal_digits, angular_decimal_digits, skip_post_process
    #print(';=====')
    #print(last_pch_point.angle.c)
    linear_decimal_digits = 5
    angular_decimal_digits = 4
    initial_c = 0.
    pch_txt = []
    loop_N_number_stack = []
    loop_number_stack = []
    cutting_tool_collection = {}
    canned_cycle_para = {'total_depth':None, 'clear_tip':None, 'dwell':None, 'inter_feed':None, 'lift_dis':None, 'tip_radius':0}
    last_pch_point = Pch_point()
    last_apt_point = Apt_point()

    block_number = 0
    gl = 9.999
    tool_number = 0
    feedrate = -999
    fixture_offset_comp = True
    skip_post_process = False

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
					'CYCLE':'CYCLE',
                    'AICC':'AICC',
                    'PPRINT':'PPRINT',
                    'FIXOFTCO':'FIXOFTCO',
                    'OPSTOP':'OPSTOP',
                    'DELAY':'DELAY',
                    'INDIRV':'INDIRV',
                    'TLON':'TLON'
                    }

    add_program_head()

    for i in apt_txt:
        #print(i)
        if re.match('SKIPPROC', i):
            skipproc(i)
        if skip_post_process:
            continue



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

        overtravel_check(i, pch_txt[-1])


    add_program_end()

    #for i in pch_txt:
    #    print(i)
    return pch_txt
