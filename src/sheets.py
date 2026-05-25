
import gspread
from google.oauth2.service_account import Credentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

def get_sheets_client():
    """
    returns an authenticated gspread client to interact with Google Sheets.
    """
    creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
    client = gspread.authorize(creds)
    return client

def test_connection(speadsheet_id):
    """
    Tests the connection to Google Sheets by writting to a sheet.
    """
    try:
        client = get_sheets_client()
        sheet = client.open_by_key(speadsheet_id)
        sheet.sheet1.update("A1", [["Test successful!"]])
        print("✓ Successfully connected to Google Sheets and updated the sheet.")
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Google Sheets: {e}")
        return False