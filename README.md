# Finance Dashboard

A comprehensive Python finance dashboard for analyzing transaction data, with automated categorization, multi-format reporting, Google Sheets integration, email notifications, and scheduled daily runs.

## Overview

This project automates financial analysis by loading bank transaction data from CSV, applying intelligent keyword-based categorization, generating comprehensive reports (text, charts, Excel), syncing to Google Sheets, and sending email summaries. It can run manually or on a daily schedule.

## Features

- **Transaction Loading**: Import transactions from CSV using `pandas`
- **Smart Categorization**: Keyword-based categorization with configurable rules
- **Multi-Format Reporting**:
  - Plain text summaries to `reports/monthly_report.txt`
  - Spending distribution charts to `reports/spending_by_category.png`
  - Excel exports with multiple worksheets
- **Google Sheets Integration**: Sync summaries, transactions, and breakdowns to Google Sheets
- **Email Notifications**: Send daily finance summary emails
- **Scheduled Automation**: Daily runs at 08:00 AM with logging
- **Data Analysis**: Calculate income, expenses, net totals, and category breakdowns

## Project Structure

```
finance-dashboard/
├── main.py                 # Entry point for manual runs
├── scheduler.py            # Automated daily scheduler
├── pyproject.toml         # Project dependencies and metadata
├── credentials.json       # Google service account (in .gitignore)
├── data/
│   └── transactions.csv   # Input transaction data
├── logs/
│   └── scheduler.log      # Scheduler execution logs
├── reports/               # Generated output files
│   ├── monthly_report.txt
│   ├── spending_by_category.png
│   ├── Finance_Dashboard.xlsx
│   └── monthly_report.xlsx
└── src/
    ├── loader.py          # CSV loading
    ├── categorizer.py     # Transaction categorization
    ├── analyser.py        # Financial analysis
    ├── reporter.py        # Text and chart reporting
    ├── Excel_reporter.py  # Excel export
    ├── sheets.py          # Google Sheets integration
    ├── email_notifier.py  # Email delivery
    ├── template_filler.py # Template processing
    └── formater.py        # Data formatting
```

## Usage

### Manual Run
Execute the dashboard once with the latest transaction data:
```bash
python main.py
```
Outputs are generated immediately to `reports/` and synced to Google Sheets and email (if configured).

### Automated Scheduler
For continuous daily automation:
```bash
python scheduler.py
```

**How it works:**
- Starts a background scheduler that runs continuously
- Executes `run_dashboard()` every day at **08:00 AM**
- Logs all runs to `logs/scheduler.log`
- Catches and logs errors without stopping the scheduler
- Press `Ctrl+C` to stop

**Typical Setup:**
- Use `python main.py` for testing or one-off analysis
- Use `python scheduler.py` in production (consider running via system task scheduler or cron)

## Configuration

Create a `.env` file in the project root with all required variables:

```
SPREADSHEET_ID=your_google_sheet_id
EMAIL_SENDER=your_email@gmail.com
EMAIL_RECEIVER=recipient@example.com
EMAIL_PASSWORD=your_app_password
```

### Google Sheets Setup
1. Create a Google Cloud project
2. Enable Google Sheets API
3. Create a service account and download `credentials.json`
4. Place `credentials.json` in the project root (add to `.gitignore`)
5. Share your Google Sheet with the service account email
6. Set `SPREADSHEET_ID` to the sheet ID from the URL

### Email Setup (Gmail with App Password)
1. Enable 2-Step Verification on your Google Account
2. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
3. write a name for the password and click crate (you can use something like`python - finance-dashboard` so you can identify where this is been used)
4. Google generates a 16-character password — copy it
5. Set in `.env`:
   ```
   EMAIL_SENDER=your_email@gmail.com
   EMAIL_PASSWORD=xxxx xxxx xxxx xxxx
   EMAIL_RECEIVER=recipient@example.com
   ```
6. If email credentials are missing, the dashboard will print a warning but continue running

## Dependencies

Main dependencies (see `pyproject.toml`):
- `pandas` - Data processing
- `matplotlib` - Chart generation
- `google-auth`, `gspread` - Google Sheets API
- `openpyxl`, `xlsxwriter` - Excel file generation
- `schedule` - Task scheduling
- `python-dotenv` - Environment configuration



## Data format

CSV must include at least these columns:

```csv
date,description,amount,type
2024-01-01,Continente Groceries,-45.50,expense
2024-01-02,Salary,3000.00,income
```

- `date`: ISO date (YYYY-MM-DD)
- `description`: transaction text from the bank
- `amount`: positive for income, negative for expenses
- `type`: optional type label (e.g. `income` / `expense`)

## Google Sheets integration

The Sheets helpers live in `src/sheets.py`. To enable:

- Add `credentials.json` to the project root (service account)
- Set `SPREADSHEET_ID` in `.env`

When configured, the project will attempt to validate the connection and can
export summary and transactions to the specified spreadsheet.

## Excel Templates

The project uses an Excel template (`Data/Finance_template.xlsx`) that gets filled with your data each run.

**Template Structure:**
- **Dashboard** sheet: Monthly summary (income, expenses, net)
- **Transactions** sheet: All categorized transactions
- **Categories** sheet: Spending breakdown by category

**How it works:**
- `src/template_filler.py` loads the blank template
- Fills in summary data, transaction rows, and category totals
- Saves to `reports/Finance_Dashboard.xlsx` after each run

**To customize:**
1. Edit `Data/Finance_template.xlsx` with your desired formatting
2. Keep the same sheet names (Dashboard, Transactions, Categories)
3. The script will populate cells with your data

## Development Notes

- **CSV Input**: Use `src/loader.py` to inspect and normalize CSV data
- **Categorization**: Update rules in `src/categorizer.py` (keyword-based matching)
- **Reports**: `src/reporter.py` generates text summaries and charts
- **Email**: `src/email_notifier.py` sends formatted summaries (gracefully skips if unconfigured)
- **Sheets**: `src/sheets.py` handles Google Sheets API integration
- **Logging**: `scheduler.py` writes operation logs to `logs/scheduler.log`

## License

Open for personal and educational use.

