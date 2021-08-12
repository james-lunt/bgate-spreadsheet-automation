#setup the google sheets api and open up all relevant sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def setup_api():
    # scope of the application
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
            "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "creds.json", scope)

    client = gspread.authorize(credentials)
    return client   

def open_sheets(client):
    return client.open("Copy of sample PDF data rows").worksheet("incoming"),client.open("PEMBERTON"),client.open("CALCO"),client.open("YANKEECANDLES"),client.open("NATURALIFE"),client.open("NATURALMED")


