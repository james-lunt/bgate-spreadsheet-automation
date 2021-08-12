#converts pdf to text
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