import fitz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import os, sys
import numpy as np

# scope of the application
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(credentials)

sheet = client.open("Tester").worksheet("Sheet2")
sheet.clear()


#convert pdf to text
at = 'test.PDF'
os.system('python -m fitz gettext test.PDF')

#create empty 2D array
empty_array = np.empty((0, 1),str)

#open covnerted text file
with open('test.txt') as f:
    #iterate through each line
    for line in f:
        #if line has values in it other than just a new character
        if line != ('\n'):
            #append line to 2D array while replacing spaces with tildas, stripping new line characters and indicating the end of a page with EOP
            empty_array = np.append(empty_array, np.array([[line.replace(' ','~').replace('\n','').replace('\x0c','EOP')]]), axis=0)


# Write the array to worksheet starting from the 1st cell
sheet.update('A1', empty_array.tolist())
#close text file
f.close()

