# main.py
# Finance Dashboard - entry point

import os
import pandas as pd
from pathlib import Path
from datetime import date
from src.loader import load_transactions
from src.categorizer import categorize_transaction
from src.reporter import print_report, save_report, save_chart
from src.analyser import summarise
from src.sheets import get_sheets_client, write_monthly_summary_to_sheet, write_transactions_to_sheet, write_category_breakdown 
from dotenv import load_dotenv

# Category rules: keyword → category
# Order matters - first match wins
categories= {
        "Groceries":     ["continente", "pingo doce", "lidl", "aldi", "mercadona", "minipreco"],
        "Utilities":     ["edp", "nos ", "vodafone", "meo ", "galp", "aguas", "gas"],
        "Transport":     ["uber", "bolt", "cp ", "metro", "carris", "galp combusti"],
        "Streaming":     ["netflix", "spotify", "youtube", "disney", "hbo"],
        "Health":        ["farmacia", "clinica", "hospital", "dentista", "saude"],
        "Food & Dining": ["restaurante", "tasca", "cafe", "mcdonald", "pizza"],
        "Shopping":      ["worten", "fnac", "zara", "primark", "amazon"],
        "Income":        ["salario", "ordenado", "mb way recebido", "transferencia recebida"],
        "Transfers":     ["mb way", "transferencia"],
    }
load_dotenv()
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


def run_dashboard():
    print("=== Finance Intelligence Dashboard ===")
    print(f"Running on: {date.today()}")
    print(f"Working directory: {Path.cwd()}")
    current_path: Path=Path.cwd()

    # Check data folder exists
    if (current_path/"data").exists():
        print("✓ Data folder found")
        if (current_path/"data"/"transactions.csv").exists():
            print("✓ Transaction file found")
        else:
            print("❌ No transaction file found in data/")
    else:
        print("❌ No data folder found")

    # Load transactions
    df=load_transactions("data/transactions.csv")
    print(df.head())  # Print the first few rows of the DataFrame for verification
    print(df.describe())  # Print summary statistics of the DataFrame for verification
    print(df.tail())  # Print the last few rows of the DataFrame for verification
    print(df.shape)  # Print the shape of the DataFrame for verification
    print(list(df.columns))  # Print the column names of the DataFrame for verification
    print(df.dtypes)  # Print the data types of the DataFrame columns for verification
    df_toalter=df.copy()  # Avoid SettingWithCopyWarning when categorizing
    #categorize and summarize transactions
    transactions_categorized=categorize_transaction(df=df_toalter, categories=categories)
    summary=summarise(transactions_categorized)
    
    # Generate reports
    os.makedirs("reports", exist_ok=True)
    print_report(summary)
    save_report(summary, current_path/"reports"/"monthly_report.txt")
    save_chart(summary, current_path/"reports"/"spending_by_category.png")
    
    # Write to Google Sheets
    print("Connecting to Google Sheets...")
    if not SPREADSHEET_ID:
        raise ValueError("SPREADSHEET_ID not found in .env file")
    try:
        gc = get_sheets_client()
        print("✓ Successfully authenticated with Google Sheets API.")
    
        moth_label = date.today().strftime("%B %Y")
        write_monthly_summary_to_sheet(SPREADSHEET_ID, summary, gc, moth_label)
        write_transactions_to_sheet(SPREADSHEET_ID, transactions_categorized, gc, moth_label)
        write_category_breakdown(gc, SPREADSHEET_ID, summary)
        print("✓ Successfully wrote to Google Sheets.")
        with pd.ExcelWriter(current_path/"reports"/"monthly_report.xlsx", engine="openpyxl") as writer:
            summary_df = pd.DataFrame([{
            "Metric": "Total Income",
            "Value (€)": summary["income"]
        }, {
            "Metric": "Total Expenses",
            "Value (€)": summary["expenses"]
        }, {
            "Metric": "Net",
            "Value (€)": summary["net"]
        }, {
            "Metric": "Transactions",
            "Value (€)": summary["transaction_count"]
        }])
            summary_df.to_excel(writer, sheet_name="Summary", index=False)
            transactions_categorized.to_excel(writer, sheet_name="Transactions", index=False)
            df.to_excel(writer, sheet_name="Raw Data", index=False)
        print("✓ Successfully wrote Excel report.")
        
    except Exception as e:
        print(f"⚠️ Sheets update failed: {e}")
        print("Local reports still saved successfully")
    
    
    print("\n✓ Dashboard complete")
if __name__ == "__main__":
    run_dashboard()
