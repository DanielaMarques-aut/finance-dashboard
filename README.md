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
├── credentials.json         # Google service account credentials
├── main.py                  # Entry point for the application
├── pyproject.toml           # Project configuration
├── README.md               # Project documentation
├── data/
│   └── transactions.csv    # Input transaction data
├── reports/
│   └── monthly_report.txt  # Generated text report
└── src/
    ├── analyser.py         # Calculates summaries and category totals
    ├── categorizer.py      # Applies category keywords to transaction descriptions
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

## Setup

1. Open a terminal and navigate to the project directory:
   ```bash
   cd finance-dashboard
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install pandas matplotlib python-dotenv gspread google-auth
   ```

4. Add your Google service account credentials file as `credentials.json`.

5. Create a `.env` file at the project root with:
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

Run the dashboard with:

```bash
python main.py
```

The script will:

- load `data/transactions.csv`
- categorize each transaction
- calculate totals and category breakdowns
- create `reports/monthly_report.txt`
- save `reports/spending_by_category.png`
- validate Google Sheets access using `SPREADSHEET_ID`

## Categories

Current categories are defined in `main.py` and include:

- `Groceries`
- `Utilities`
- `Transport`
- `Streaming`
- `Health`
- `Food & Dining`
- `Shopping`
- `Income`
- `Transfers`
- `Uncategorized`

## Google Sheets Integration

The project uses `credentials.json` and `SPREADSHEET_ID` to connect to Google Sheets via the Sheets API.

- `src/sheets.py` authenticates with `gspread`
- `main.py` calls `test_connection` to verify access

## Development Notes

- `src/loader.py` loads and normalizes transaction CSV data
- `src/categorizer.py` applies keyword-based categorization
- `src/analyser.py` computes totals, category sums, and biggest expense
- `src/reporter.py` prints the report, saves a text file, and generates charts

### Extending Categories

Add or modify keywords in `main.py` or update `src/categorizer.py` with new category mappings.

## License

Open source and available for personal or educational use.
