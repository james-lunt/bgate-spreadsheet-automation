import fitz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import os

# scope of the application
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(credentials)

sheet = client.open("Tester").worksheet("Sheet1")

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
       insertRow = [line]
       sheet.insert_row(insertRow, 1)
       #print (line)




