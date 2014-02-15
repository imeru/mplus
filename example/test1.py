origin = open('idf_sample/demo.idf', 'r')
for line in origin:
    line = line.replace("U-Factor", "@@U-FACTOR@@")
    print line
origin.close()
