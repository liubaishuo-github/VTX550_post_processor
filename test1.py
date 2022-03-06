import re

class Cutting_Tool():
    def __init__(self, pocket, data_number):
        with open(r'C:\Users\asus\Desktop\aaa.txt', encoding='utf-8-sig') as file:
            lines = file.readlines()
        self.pocket = pocket
        self.data_number = data_number
        self.gauge_length = 10
        self.radius = ''
        self.code = 'PCZ'
        self.name = 'TBEM'
        self.haha = lines


cutting_tool_collection = {}
apt = 'TOOLNO/30,212.3'
tool_pocket = re.search('\d+', apt[:apt.find(',')]).group()
tool_data_number = re.search('\d+\.?\d+', apt[apt.find(',')+1 :]).group()

tool_instance = Cutting_Tool(tool_pocket, tool_data_number)

print(type(tool_instance))

cutting_tool_collection[tool_pocket] = tool_instance
print(cutting_tool_collection[tool_pocket].gauge_length)
