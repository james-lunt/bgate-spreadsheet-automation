import fitz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import os
import numpy as np

# scope of the application
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(credentials)

sheet = client.open("Tester").worksheet("Sheet2")
sheet.clear()

empty_array = np.empty((0, 1),str)
with open('out.txt') as f:
   
   #first = True
   for line in f:
       empty_array = np.append(empty_array, np.array([[line]]), axis=0)

#print(empty_array) 

# Write the array to worksheet starting from the 1st cell
sheet.update('A1', empty_array.tolist())

"""
at = 'test.PDF'
os.system('python -m fitz gettext -pages 1 test.PDF')

#input file
fin = open("test.txt", "rt")
fout = open("out.txt", "wt")
 
for line in fin:
	fout.write(line.replace(' ', '~'))

fin.close()
fout.close()

with open('out.txt') as f:
   for line in f:
    #insertRow = [line]
    #sheet.insert_row(insertRow, 1)
       print (line)
"""





