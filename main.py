#Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import fitz
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import os, sys
import numpy as np
import requests


#----------------------------------Setup API-------------------------------------------------
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(credentials)




#---------------------------------Check for new invoices------------------------------------
#Open inbound invoices sheet
invoices = client.open("Copy of sample PDF data rows").worksheet("incoming")

current_rows = len(invoices.col_values(1))
#infinite loop to check for new invoices
while(True):
    if len(invoices.col_values(1)) > current_rows:
        index = invoices.col_values(1)
        break 




#---------------------Download PDF from url and Convert to text-----------------------------
pdf_name = invoices.cell(index, 6).value
pdf = requests.get(pdf_name, allow_redirects=True)

#convert pdf to text
os.system('python -m fitz gettext %s',pdf)




#---------------------Tilda parse data and write it to google sheets-----------------------
#create empty 2D array
empty_array = np.empty((0, 1),str)

#open converted text file
with open(os.system('python -m fitz gettext %s',pdf)) as f:
    #iterate through each line
    for line in f:
        #if line has values in it other than just a new character
        if line != ('\n'):
            #append line to 2D array while replacing spaces with tildas, stripping new line characters and indicating the end of a page with EOP
            empty_array = np.append(empty_array, np.array([[line.replace(' ','~').replace('\n','').replace('\x0c','EOP')]]), axis=0)

#Open Outbound invoices sheet
outbound = client.open("Output").worksheet("Sheet1")

# Write the array to worksheet starting from the 1st cell
outbound.update('A1', empty_array.tolist())
#close text file
f.close()