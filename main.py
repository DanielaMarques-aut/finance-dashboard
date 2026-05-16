
def main():
# main.py
# Finance Dashboard - entry point

   
    from pathlib import Path
    from datetime import date
    from src.loader import load_transactions
    from src.categorizer import categorize_all_transactions
    from src.reporter import print_report, save_report
    from src.analyser import summarize_transactions


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
    transactions: list[dict[str, str]]=load_transactions(current_path/"data"/"transactions.csv")
    print(transactions[0])  # Print the first transaction for verification
    transactions_categorized=categorize_all_transactions(transactions)
    summary=summarize_transactions(transactions=transactions_categorized)
    print_report(summary)
    save_report(summary, current_path/"reports"/"monthly_report.txt")

if __name__ == "__main__":
    main()
