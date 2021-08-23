#Imports
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import fitz
from pprint import pprint
import os, sys
import numpy as np
import requests
import time
import datetime


#----------------------------------Setup API-------------------------------------------------
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(credentials)

#open admin sheet
admin = client.open("sample PDF data rows").worksheet("admin")
admin_values = admin.get_all_values()


#---------------------------------Check for new invoices------------------------------------
#open invoice sheet
invoices = client.open("sample PDF data rows").worksheet("incoming")
invoice_values = invoices.get_all_values()

#count spreadsheet rows for indexing    
row_counter = 1 
#counts the number invoices being processed
#sleep_count = 0
for invoice in invoice_values:
    time.sleep(10)
    if invoice[6] == 'TRUE':
        """
        print(sleep_count)
        #every 10 procedures sleep
        if sleep_count == 5:
        sleep_count+=1
        """

        #get url and name for pdf
        pdf_name = invoice[1]
        pdf_url = invoice[3]
        pdf_short_url = invoice[2]
        #get the supppliers name
        invoice_supplier = invoice[5]


        #------------------------------------Download and Convert PDF------------------------------
        r = requests.get(pdf_url, allow_redirects=True)
        #write pdf to local machine with correct name
        open(pdf_name, 'wb').write(r.content)


        #convert pdf to text
        os.system('python -m fitz gettext {}'.format(pdf_name))
        #to find converted text file on local machine
        text_name = pdf_name.replace('.PDF', '.txt')


        #---------------------Tilda parse data and write it to google sheets-----------------------
        #create 2D array with pdf name and short url as the first entries
        empty_array = np.array([[pdf_name],[pdf_short_url]])
        #open converted text file
        with open(text_name) as f:
            #iterate through each line
            for line in f:
                #if line has values in it other than just a new character
                if line != ('\n'):
                    #append line to 2D array while replacing spaces with tildas, stripping new line characters and indicating the end of a page with EOP
                    empty_array = np.append(empty_array, np.array([[line.replace(' ','~').replace('\n','').replace('\x0c','EOP')]]), axis=0)


        #search admin sheet for destination sheet
        for i in admin_values:
            #if supplier label matches
            if i[0] == invoice_supplier:
                #open respective worksheet
                dest = client.open_by_key(i[1]).worksheet("Sheet1")
                #clear sheet of previous input
                dest.clear()
                #write parsed data to sheet
                dest.update('A1',empty_array.tolist())
                break


        #set check to false on invoices sheet
        invoices.update_cell(row_counter,7,'FALSE')

        #-----------------------------Delete text and pdf off local machine----------------------- 
        os.remove(text_name)
        os.remove(pdf_name)

    #count spreadsheet rows for indexing    
    row_counter+=1

    #loop