# Finance Dashboard

A Python-based dashboard for analyzing bank transaction data, generating monthly spending reports, visual charts, and validating Google Sheets access.

## Features

- Load transactions from CSV using `pandas`
- Automatically categorize expenses using keyword matching
- Summarize income, expenses, net balance, and spending by category
- Export a text report and a visual spending chart
- Connect to Google Sheets using service account credentials

## Project Structure

```
finance-dashboard/
├── credentials.json         # Google service account credentials for Sheets API
├── main.py                  # Entry point for the application
├── pyproject.toml           # Project configuration and dependencies
├── README.md                # Project documentation
├── data/
│   └── transactions.csv     # Input transaction data
├── reports/
│   ├── monthly_report.txt   # Generated text report
│   └── spending_by_category.png # Generated chart
└── src/
    ├── analyser.py         # Calculates summaries and category totals
    ├── categorizer.py      # Applies keyword-based categorization
    ├── loader.py           # Loads transaction CSV files into pandas
    ├── reporter.py         # Prints, saves, and charts report data
    └── sheets.py           # Google Sheets integration helpers
```

## Requirements

- Python 3.12 or higher
- `pandas`
- `matplotlib`
- `python-dotenv`
- `gspread`
- `google-auth`
- `dotenv`

## Installation

1. Clone the repository:   git clone https://github.com/yourusername/finance-dashboard.git
      

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
   pip install -r requirements.txt
   ```

   If a `requirements.txt` file is not available, install directly:
   ```powershell
   pip install pandas matplotlib python-dotenv gspread google-auth
   ```

4. Add your Google service account credentials as `credentials.json` in the project root.

5. Create a `.env` file at the project root and set your spreadsheet ID:
   ```env
   SPREADSHEET_ID=your_google_sheet_id
   ```

## Data Format

The transaction CSV should be placed at `data/transactions.csv` and include at least these columns:

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
- compute summaries and category totals
- save `reports/monthly_report.txt`
- save `reports/spending_by_category.png`
- validate Google Sheets access using `SPREADSHEET_ID`

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

`main.py` calls `test_connection(SPREADSHEET_ID)` to validate access.

## Development Notes

- `src/loader.py`: loads and normalizes CSV transaction data
- `src/categorizer.py`: applies category matching rules
- `src/analyser.py`: computes totals, category summaries, and highest expenses
- `src/reporter.py`: prints report output, saves report text, and generates charts
- `src/sheets.py`: manages Google Sheets authentication and access tests

## Notes

- Ensure `data/transactions.csv` exists before running `main.py`.
- `reports/` is created automatically if needed.

## License

Open source and available for personal or educational use.
