#Splits the invoice pdf to seperate spreadsheets for each client
#imports
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

import requests
import urllib


url = 'https://drive.google.com/uc?id=15Zqk5A1BEOdeC2aDwVuVzTcqjYJb_Igr&export=download'
r = requests.get(url, allow_redirects=True)

open('INVOICE', 'wb').write(r.content)

"""
# scope of the application
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(credentials)

# Open the spreadhseet
sheet = client.open("Copy of sample PDF data rows").worksheet("incoming")
"""

#Extracts text from pdf and puts it into python variable
output_string = StringIO()
with open('INVOICE', 'rb') as in_file:
    parser = PDFParser(in_file)
    doc = PDFDocument(parser)
    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    for page in PDFPage.create_pages(doc):
        interpreter.process_page(page)


print(output_string.getvalue())
