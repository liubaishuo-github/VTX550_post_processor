import re
str_1=r'$$ PERATION NAME : Tool Change.1'
key = r'\$\$ PERATION NAME'
nPos= re.match(key,str_1)
print(nPos)
