# Finance Dashboard

A Python finance dashboard for analyzing transaction CSV data, categorizing expenses, generating summary reports, and validating Google Sheets access.

## Overview

This project loads bank transaction data from `data/transactions.csv`, applies keyword-based categorization, summarizes totals and category spending, saves a plain-text report, generates a chart, and verifies Google Sheets connectivity using a service account.

## Features

- Load transaction data from CSV using `pandas`
- Categorize transactions using keyword matching
- Summarize income, expenses, net totals, and spending by category
- Save report output to `reports/monthly_report.txt`
- Generate spending chart at `reports/spending_by_category.png`
- Validate Google Sheets access via service account credentials

## Project Structure

```
finance-dashboard/
├── credentials.json             # Google service account credentials for Sheets API
├── main.py                      # Entry point for the application
├── pyproject.toml               # Project configuration and dependencies
├── README.md                    # Project documentation
├── data/
│   └── transactions.csv         # Input transaction data
├── reports/
│   ├── monthly_report.txt       # Generated text report
│   └── spending_by_category.png # Generated chart
└── src/
    ├── analyser.py             # Calculates summaries and category totals
    ├── categorizer.py          # Applies keyword-based categorization
    ├── loader.py               # Loads transaction CSV files into pandas
    ├── reporter.py             # Prints, saves, and charts report data
    └── sheets.py               # Google Sheets integration helpers
```

## Requirements

- Python 3.12 or higher
- `pandas`- data analysis library
- `matplotlib` - chart creation and visualization library
- `python-dotenv` - loads environment variables from `.env` files
- `gspread` - Google Sheets API client library
- `google-auth` - Authentication library for Google APIs

## Dependencies


Dependencies are declared in `pyproject.toml`. A `requirements.txt` file is not currently included in this repository.

## Setup

1. Open a terminal and navigate to the project directory:
   ```powershell
   cd C:\Users\username\finance-dashboard
   ```

2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install pandas matplotlib python-dotenv gspread google-auth
   ```

4. Add your Google service account credentials file as `credentials.json` in the project root.

5. Create a `.env` file in the project root and add:
   ```env
   SPREADSHEET_ID=your_google_sheet_id
   ```

## Data Format

Place a CSV file at `data/transactions.csv` with the following columns:

```csv
date,description,amount,type
2024-01-01,Continente Groceries,-45.50,expense
2024-01-02,Salário Monthly Income,3000.00,income
```

- `date`: transaction date
- `description`: bank description text
- `amount`: positive for income, negative for expenses
- `type`: transaction type label

## Usage

Run the dashboard:

```powershell
python main.py
```

The script will:

- load transactions from `data/transactions.csv`
- apply keyword-based categorization
- compute totals and category breakdowns
- Generates monthly summary reports (terminal + text file)
- Creates spending breakdown charts (bar + pie)
- save `reports/monthly_report.txt`
- save `reports/spending_by_category.png`
- validate Google Sheets access using `SPREADSHEET_ID`
- **Syncs automatically to Google Sheets** ← new
  - Monthly summary tab
  - Full transaction history tab  

## Category Rules

Category keywords are defined in `main.py`. Current categories include:

- `Groceries`
- `Utilities`
- `Transport`
- `Streaming`
- `Health`
- `Food & Dining`
- `Shopping`
- `Income`
- `Transfers`

Transactions that do not match any keyword are assigned `Uncategorized`.

## Google Sheets Integration

The Sheets integration is handled in `src/sheets.py` and requires:

- `credentials.json` service account file
- `SPREADSHEET_ID` set in `.env`

`main.py` loads environment variables and calls `test_connection(SPREADSHEET_ID)` to verify access.

## Development Notes

- `src/loader.py`: loads and normalizes CSV transaction data
- `src/categorizer.py`: applies keyword-based categorization rules
- `src/analyser.py`: computes totals, category summaries, and key metrics
- `src/reporter.py`: prints report output and saves report files
- `src/sheets.py`: manages Google Sheets authentication and connection 

## Notes

- Ensure `data/transactions.csv` exists before running `main.py`.
- `reports/` is created automatically if needed.

## License

Open source and available for personal or educational use.
