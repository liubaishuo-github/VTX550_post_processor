import re

class Cutting_Tool():
    def __init__(self, pocket, data_number):
        self.pocket = pocket
        self.data_number = data_number
        self.gauge_length = 10
        self.radius = ''
        self.code = 'PCZ'
        self.name = 'TBEM'
    def extract_tool_info(self):
        print(self.data_number)
        print(self.pocket)


apt = 'TOOLNO/30,212.3'
tool_pocket = re.search('\d+', apt[:apt.find(',')]).group()
tool_data_number = re.search('\d+\.?\d+', apt[apt.find(',')+1 :]).group()

tool_instance = Cutting_Tool(tool_pocket, tool_data_number)
tool_instance.extract_tool_info()

print(tool_instance.name)
