import re

origin = open('idf_sample/demo.idf', 'r')
for line in origin:
    line = line.replace("U-Factor", "@@U-FACTOR@@")
    print line
    if "@@U-FACTOR@@" in line:
        print re.search(r'[-+]?\d*\.\d+|s\d+', line).group()
origin.close()

