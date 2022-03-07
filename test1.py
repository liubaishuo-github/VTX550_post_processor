import re

apt = 'AICC/ON,10'
if re.search('\d+', apt):
    level = re.search('\d+', apt).group()
else:
    level = '1'
print(level)
