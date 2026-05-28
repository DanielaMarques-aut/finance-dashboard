

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

def write_monthly_summary_to_sheet(spreadsheet_id, summary, gc, month_label):
    """
    Writes the monthly summary to a Google Sheet called summary.
    Creates a new sheet for the month if it doesn't exist, or updates the existing one.
    """
    # Connect to the spreadsheet and select or create the summary sheet
    try:
        client = get_sheets_client()
        sheet = client.open_by_key(spreadsheet_id)
        # Convert summary to a list of lists for gspread
        worksheet= sheet.worksheet("Summary")
    
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title="Summary", rows="100", cols="10")
    except Exception as e:
        print(f"❌ Failed to access or create the Summary sheet: {e}")
        return False
    # If the sheet is empty, add headers
    if not worksheet.get_all_values():
        worksheet.update("A1:E1", [[
            "Month", "Income (€)", "Expenses (€)", 
            "Net (€)", "Transactions"
        ]])
        #Bold the header row
        worksheet.format("A1:E1", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}})

        #append this moth's summary
    try:
        worksheet.append_row([
            month_label,
            summary["Income"],
            summary["Expenses"],    
            summary["Net"],
            summary["Transaction_Count"]
        ])

        print("✓ Successfully wrote monthly summary to Google Sheets.")
    except Exception as e:
        print(f"❌ Failed to write monthly summary to Google Sheets: {e}")

def write_transactions_to_sheet(spreadsheet_id, df, gc, month_label):
    """
    Writes the transactions to a transactions Google Sheet.
    Creates a new sheet for the month if it doesn't exist, or updates the existing one.
    """
    # Connect to the spreadsheet and select or create the month sheet
    try:
        client = get_sheets_client()
        sheet = client.open_by_key(spreadsheet_id)
        worksheet = sheet.worksheet("Transactions")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title="Transactions", rows="100", cols="10")
    except Exception as e:
        print(f"❌ Failed to access or create the Transactions sheet: {e}")
        return False
    headers = ["Date","Description","Amount","Category"]
    # If the sheet is empty, add headers
    if not worksheet.get_all_values():
        worksheet.update("A1:E1", [headers])
        #Bold the header row
        worksheet.format("A1:E1", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}})
  # Prepare data
        df_export = df[["date", "description", "amount", "category"]].copy()
        df_export["date"] = df_export["date"].dt.strftime("%Y-%m-%d")
    # Convert transactions to a list of lists for gspread
    transaction_rows =  df_export.values.tolist()
    worksheet.update(f"A1:D{len(transaction_rows)}", transaction_rows)
    # Append transactions
    try:
        worksheet.append_rows(transaction_rows)
        print(f"✓ Successfully wrote transactions for {month_label} to Google Sheets.")
    except Exception as e:
        print(f"❌ Failed to write transactions for {month_label} to Google Sheets: {e}")
    # Colour expenses red, income green
    try:
        for i, row in enumerate(transaction_rows, start=2):  # Start from row 2 to skip headers
            amount = row[2]  # Assuming amount is in the third column (C)
            if amount < 0:
                worksheet.format(f"C{i}", {"backgroundColor": {"red": 1, "green": 0.8, "blue": 0.8}})
            else:
                worksheet.format(f"C{i}", {"backgroundColor": {"red": 0.8, "green": 1, "blue": 0.8}})
        print("✓ Successfully formatted transaction amounts in Google Sheets.")
    except Exception as e:
        print(f"❌ Failed to format transaction amounts in Google Sheets: {e}")

def write_category_breakdown (gc,spreadsheet_id, summary):
    """Writes spending by category to a Categories tab."""
    # Connect to the spreadsheet and select or create the category breakdown sheet
    client = get_sheets_client()
    sheet = client.open_by_key(spreadsheet_id)
    try:
        worksheet = sheet.worksheet("Categories")
    except gspread.exceptions.WorksheetNotFound:
        worksheet = sheet.add_worksheet(title="Categories", rows="50", cols="5")
    except Exception as e:
        print(f"❌ Failed to access or create the Categories sheet: {e}")
        return False
    headers = ["Category", "Amount (€)", "Percentage of Expenses"]
    # If the sheet is empty, add headers
    if not worksheet.get_all_values():
        worksheet.update("A1:C1", [headers])
        #Bold the header row
        worksheet.format("A1:C1", {"textFormat": {"bold": True}})
    total_expenses=summary["Expenses"]
    # Calculate percentage of total expenses for each category
    # Prepare data
    category_rows = []
    for category, amount in summary["By_Category"].items():
        percentage = round((amount / total_expenses) * 100, 1) if total_expenses > 0 else 0
        category_rows.append([category,round(amount, 2), f"{percentage}%"])
    try:
        worksheet.update(f"A2:C{len(category_rows)+1}", category_rows)
        print(f"✓ Successfully wrote category breakdown {len(category_rows)} to Google Sheets.")
    except Exception as e:
        print(f"❌ Failed to write category breakdown {len(category_rows)} to Google Sheets: {e}")