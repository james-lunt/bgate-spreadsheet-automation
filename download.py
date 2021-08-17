import fitz

import os
at = 'test.PDF'
os.system('python -m fitz gettext -pages 1 test.PDF')

my_file = open("test.txt", "r")
for line in my_file:
    print(line)

#for line in my_file:
	#read replace the string and write to output file
#	my_file.write(line.replace(' ', '~'))

