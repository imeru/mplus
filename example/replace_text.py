origin = open('idf_sample/simple.idf', 'r')
new = open('idf_sample/simple.idf.tmp', 'w')
for line in origin:
    new.write(line.replace('@@Height@@', '1000'))
origin.close()
new.close()
