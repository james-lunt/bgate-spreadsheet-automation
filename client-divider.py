# Splits the invoice pdf to seperate spreadsheets for each client
from io import StringIO
import requests
import urllib
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint


# scope of the application
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(credentials)


# Client spreadsheets spreadhseet
invoices = client.open("Copy of sample PDF data rows").worksheet("incoming")
pemberton_sheet = client.open("PEMBERTON")
calco_sheet = client.open("CALCO")
yankeecandles_sheet = client.open("YANKEECANDLES")
naturallife_sheet = client.open("NATURALIFE")
naturalmed_sheet = client.open("NATURALMED")

# row we're working with
index = 1

# creates a new sheet on the suppliers spreadsheet for a new invoice
def new_invoice(supplier, supplier_sheet):
    file_name = invoices.col_values(2)
    supplier_sheet.add_worksheet(title=file_name[index], rows="100", cols="20")

#identifies the supplier and calls new_invoice with the according parameters
def identify_supplier():
    supplier = invoices.col_values(6)
    pprint(supplier[index])
    if supplier[index] == 'PEMBERTON':
        new_invoice(supplier, pemberton_sheet)
    if supplier[index] == 'CALCO':
        new_invoice(supplier, calco_sheet)
    if supplier[index] == 'YANKEECANDLES':
        new_invoice(supplier, yankeecandles_sheet)
    if supplier[index] == 'NATURALIFE':
        new_invoice(supplier, naturallife_sheet)
    if supplier[index] == 'NATURALMED':
        new_invoice(supplier, naturalmed_sheet)

identify_supplier()
