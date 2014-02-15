import re

origin = open('idf_sample/demo.idf', 'r')
for line in origin:
    if "U-Factor" in line:
        print re.search(r'[-+]?\d*\.\d+|\d+', line).group()
origin.close()
