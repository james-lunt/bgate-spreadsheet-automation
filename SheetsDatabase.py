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

# Get a list of all records
data = sheet.get_all_records()
#pprint(data)

current_rows = len(sheet.col_values(1))
pprint("Start")
while(True):
    if len(sheet.col_values(1)) > current_rows:
        print("yes")
        break 

pprint("done")
