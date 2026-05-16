# Finance Dashboard

A Python-based financial analysis tool that loads transaction data, categorizes expenses, and generates detailed monthly financial spending reports.

## Features

- **Transaction Loading**: Import transactions from CSV files exported from Portuguese banks.
- **Smart Categorization**: Automatically categorize transactions using keyword matching (groceries, utilities, transport...)
- **Financial Analysis**: Calculate income, expenses, and net balance
- **Spending Breakdown**: View expenses organized by category with visual representations
- **Report Generation**: Generate both console and file-based financial summary reports
- Modular structure — easy to extend 

## Project Structure

```
finance-dashboard/
├── main.py                 # Entry point for the application
├── pyproject.toml         # Project configuration
├── README.md              # This file
├── data/
│   └── transactions.csv   # CSV file containing transaction data
├── reports/
│   └── monthly_report.txt # Generated monthly financial report
└── src/
    ├── loader.py         # Loads transactions from CSV
    ├── categorizer.py    # Categorizes transactions by keyword
    ├── analyser.py       # Analyzes transactions and calculates summary
    └── reporter.py       # Generates formatted reports
```

## Installation

### Requirements
- Python 3.12 or higher
no external dependencies required

### Setup

1. Clone or download the project
2. Navigate to the project directory:
   ```bash
   cd finance-dashboard
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   source .venv/bin/activate  # On macOS/Linux
   ```

4. Install dependencies (if any are added later):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Preparing Your Data

1. Create a `data/` directory if it doesn't exist
2. Export transactions from your bank as CSV
or
3. Add a `transactions.csv` file with the following format:
   ```
   date,description,amount,type
   2024-01-01,Continente Groceries,-45.50,expense
   2024-01-02,Salário Monthly Income,3000.00,income
   ```
3. Place the file in `data/transactions.csv`
### Running the Application

```bash
python main.py
```

The application will:
- Load transactions from `data/transactions.csv`
- Categorize each transaction based on keywords
- Generate a financial summary with:
  - Total income
  - Total expenses
  - Net balance (income - expenses)
  - Spending breakdown by category
- Display the report in the console
- Save the report to `reports/monthly_report.txt`

## Supported Categories

Transactions are automatically categorized into:
- **Groceries**: Supermarkets (Continente, Pingo Doce, Lidl, etc.)
- **Utilities**: Energy, internet, water providers (EDP, NOS, Vodafone, etc.)
- **Transport**: Uber, Bolt, public transit, fuel
- **Streaming**: Netflix, Spotify, YouTube, Disney+, HBO
- **Health**: Pharmacies, clinics, hospitals, dentists
- **Food & Dining**: Restaurants, cafés, fast food
- **Shopping**: Electronics, clothing, online stores
- **Income**: Salary, transfers received
- **Transfers**: Money transfers (MB Way, transfers)
- **Uncategorized**: Transactions that don't match any keyword

## Example Output

```
=== Finance Intelligence Dashboard ===
Running on: 2024-01-15
Working directory: C:\Users\username\finance-dashboard

✓ Data folder found
✓ Transaction file found
✓ Loaded 25 transactions from data/transactions.csv

=============================================
   MONTHLY FINANCE REPORT
   Generated on: 2024-01-15
=============================================
Income:..................+3000.00€
Expenses:...............-542.35€
Net:...................2457.65€

Spending by Category:
  Groceries          142.50€  ██████████████
  Transport           89.25€  ████████
  Food & Dining      145.60€  ██████████████
  Utilities           95.00€  █████████
  Shopping           70.00€  ███████
=============================================

✓ Report saved to reports/monthly_report.txt
```

## Development

### Module Overview

- **loader.py**: Reads CSV transactions with error handling
- **categorizer.py**: Matches transaction descriptions against keyword rules
- **analyser.py**: Calculates financial metrics and category summaries
- **reporter.py**: Formats and outputs reports to console and file

### Extending Categories

Edit `src/categorizer.py` to add new categories or keywords:

```python
categories = {
    "Your Category": ["keyword1", "keyword2", "keyword3"],
    # ... other categories
}
```

## Notes

- Amounts in CSV should be positive for income and negative for expenses
- The keyword matching is case-insensitive
- First matching keyword wins (order matters in the categories dictionary)
- Reports are generated in Euro (€) currency format

## License

This project is open source and available for personal and educational use.
