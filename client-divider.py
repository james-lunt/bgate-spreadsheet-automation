# Splits the invoice pdf to seperate spreadsheets for each client
from setupAPI import *
from io import StringIO
import requests
import urllib 
from pprint import pprint

# row we're working with
index = 1

#API initialisation
client = setup_api()
#open sheets
invoices,pemberton_sheet,calco_sheet,yankeecandles_sheet,naturallife_sheet,naturalmed_sheet = open_sheets(client)

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
