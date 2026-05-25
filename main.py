
def main():
# main.py
# Finance Dashboard - entry point

    import os
    from pathlib import Path
    from datetime import date
    from src.loader import load_transactions
    from src.categorizer import categorize_transaction
    from src.reporter import print_report, save_report
    from src.analyser import summarise
    from src.reporter import save_chart
    from src.sheets import test_connection
    from dotenv import load_dotenv



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
    transactions_categorized=categorize_transaction(df=df, categories=categories)
    summary=summarise(transactions_categorized)
    os.makedirs("reports", exist_ok=True)
    print_report(summary)
    save_report(summary, current_path/"reports"/"monthly_report.txt")
    save_chart(summary, current_path/"reports"/"spending_by_category.png")
    load_dotenv()
    SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

    if not SPREADSHEET_ID:
        raise ValueError("SPREADSHEET_ID not found in .env file")
    test_connection(SPREADSHEET_ID)
if __name__ == "__main__":
    main()
