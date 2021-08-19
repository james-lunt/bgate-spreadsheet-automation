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
invoices = client.open("sample PDF data rows").worksheet("incoming")
invoice_values = invoices.get_all_values()
process_list = []
for invoice in invoice_values:
    #Boolean value in column 6
    if invoice[6] == 'TRUE':
        process_list.append(invoice)

#print(process_list)


#------------------------------------Download and Convert PDF------------------------------
for invoice in process_list:
    #get url and name for pdf
    pdf_name = invoice[1]
    pdf_url = invoice[3]
    #download pdf   
    r = requests.get(pdf_url, allow_redirects=True)
    #write pdf to local machine with correct name
    open(pdf_name, 'wb').write(r.content)


    #convert pdf to text
    os.system('python -m fitz gettext {}'.format(pdf_name))

    text_name = pdf_name.replace('.PDF', '.txt')


#---------------------Tilda parse data and write it to google sheets-----------------------
    #create empty 2D array
    empty_array = np.empty((0, 1),str)

    #open converted text file
    with open(text_name) as f:
        #iterate through each line
        for line in f:
            #if line has values in it other than just a new character
            if line != ('\n'):
                #append line to 2D array while replacing spaces with tildas, stripping new line characters and indicating the end of a page with EOP
                empty_array = np.append(empty_array, np.array([[line.replace(' ','~').replace('\n','').replace('\x0c','EOP')]]), axis=0)

    #Open Outbound invoices sheet
    outbound = client.open("Output").worksheet("Sheet1")
    outbound.clear() #clear sheet for testing

    # Write the array to worksheet starting from the 1st cell
    outbound.update('A1', empty_array.tolist())
    #close text file
    f.close()

#-----------------------------Delete text and pdf off local machine-----------------------
    os.remove(text_name)
    os.remove(pdf_name)
