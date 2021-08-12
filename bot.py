import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

# scope of the application
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    "creds.json", scope)

client = gspread.authorize(credentials)

# Open the spreadhseet
sheet = client.open("Copy of sample PDF data rows").worksheet("incoming")
insertRow = ["GA111A28J-A11","Gabor","Trainers — weiß/ice","https://img01.ztat.net/article/spp-media-p1/bc1c433d1649346e9eb02d316961bfc9/dd8d3ad466d64631b956405046eb9ca1.jpg","£89.99","https://www.zalando.co.uk/gabor-trainers-weissice-ga111a28j-a11.html"]
sheet.insert_row(insertRow, 8)