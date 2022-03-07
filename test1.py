import re

apt = 'TOOLNO/13,141.3'
print(apt[apt.find(',')+1 :])
print('============')
tool_data_number = re.search('(\d+\.?\d+|\d+)', apt[apt.find(',')+1 :]).group()
print(tool_data_number)
