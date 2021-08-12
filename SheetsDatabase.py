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
# Insert the list as a row at index 8
#insertRow = ["GA111A28J-A11","Gabor","Trainers — weiß/ice","https://img01.ztat.net/article/spp-media-p1/bc1c433d1649346e9eb02d316961bfc9/dd8d3ad466d64631b956405046eb9ca1.jpg","£89.99","https://www.zalando.co.uk/gabor-trainers-weissice-ga111a28j-a11.html"]
#sheet.insert_row(insertRow, 8)

# Get a specific row
#row = sheet.row_values(3)
#pprint(row)


# Update one cell
#sheet.update_cell(8, 2, "ADIDAS")

# Get a specific column
#col = sheet.col_values(3)
#pprint(col)

# Delete the row
#sheet.delete_row(8)
