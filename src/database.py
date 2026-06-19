import sqlite3
import os
DB_PATH = "data/finance.db"

def get_db_connection():
    """Establishes a connection to the SQLite database."""
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def initialize_database():
    """Initializes the database with the transactions table."""
    conn = get_db_connection() # Connect to the database, creating it if it doesn't exist
    cursor = conn.cursor() # Allows us to execute SQL commands
    # Create the transactions table if it doesn't exist
    #Transactins tabele has id, date, description, amount, category, type (income/expense), month and created_at timestamp
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT DEFAULT "Uncategorized",
            "type" TEXT,
            Month TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Ensure a uniqueness constraint for (date, description, amount) to avoid duplicates
    try:
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_transactions_unique ON transactions(date, description, amount)")
    except Exception:
        pass
    #monthly summary table has id, month, income, expenses, net, transaction_count and created_at timestamp
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monthly_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Month TEXT NOT NULL,
    income REAL,
    expenses REAL,
    net REAL,
    transaction_count INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    # Ensure Month is unique so upserts can work and duplicates are prevented
    try:
        cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_monthly_summary_month_unique ON monthly_summary(Month)")
    except Exception:
        pass
    # Commit the changes and close the connection
    conn.commit()
    # Backfill Month for existing rows where it's missing using the date (YYYY-MM)
    try:
        cursor.execute("""
        UPDATE transactions
        SET Month = substr(date, 1, 7)
        WHERE Month IS NULL OR Month = ''
        """)
        conn.commit()
    except Exception:
        pass
    # Remove any existing duplicate rows (keep the first row per date/description/amount)
    try:
        cursor.execute("""
        DELETE FROM transactions
        WHERE rowid NOT IN (
            SELECT MIN(rowid) FROM transactions
            GROUP BY date, description, amount
        )
        """)
        conn.commit()
    except Exception:
        pass
    # Remove duplicate monthly_summary rows (keep earliest id per Month)
    try:
        cursor.execute("""
        DELETE FROM monthly_summary
        WHERE id NOT IN (
            SELECT MIN(id) FROM monthly_summary
            GROUP BY Month
        )
        """)
        conn.commit()
    except Exception:
        pass
    # Ensure created_at filled for old rows
    try:
        cursor.execute("UPDATE monthly_summary SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL OR created_at = ''")
        conn.commit()
    except Exception:
        pass
    conn.close()
    print("✓ Database initialized successfully.")

def get_info():
    """Fetches all transactions from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    cursor.execute("""
    SELECT MIN(date), MAX(date) FROM transactions
    """)
    date_range = cursor.fetchone()
    conn.close()
    print(f"✓ Database {DB_PATH} contains {count} transactions")
    if date_range[0] and date_range[1]:
        print(f"✓ Transactions date range: {date_range[0]} to {date_range[1]}")
    else:
        print("✓ No transactions found in the database.")

def import_from_df(df):
    """Imports transactions from a DataFrame into the database.
    Skips duplicates based on date, description and amount."""
    conn = get_db_connection()
    cursor = conn.cursor()
    imported_count = 0
    skipped_count = 0

    for _, row in df.iterrows():
        # Normalize values to avoid false negatives when checking duplicates
        date_str = str(row.get("date"))[:10]
        description = (row.get("description") or "").strip()
        try:
            amount_val = round(float(row.get("amount") or 0), 2)
        except Exception:
            amount_val = 0.0

        # Check if exists
        cursor.execute("""
            SELECT COUNT(*) FROM transactions
            WHERE date=? AND description=? AND amount=?
        """, (date_str, description, amount_val))
        count = cursor.fetchone()[0]
        if count:
            skipped_count += 1
            continue

        # Insert using normalized values; rely on unique index as a safety net
        cursor.execute("""
            INSERT OR IGNORE INTO transactions (date, description, amount, category, "type", Month)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            date_str,
            description,
            amount_val,
            row.get("category", "Uncategorized"),
            row.get("type", "debit") or row.get("Type", "debit"),
            row.get("Month", row.get("date").strftime("%Y-%m") if row.get("date") is not None else None)
        ))
        # If row was ignored due to unique constraint, count as skipped
        if cursor.rowcount == 0:
            skipped_count += 1
        else:
            imported_count += 1

    conn.commit()
    conn.close()
    print(f"✓ Imported {imported_count} transactions into the database.")
    print(f"✓ Skipped {skipped_count} duplicate transactions.")
    return imported_count, skipped_count

def get_all_transactions(Month=None):
    """Fetches all transactions from the database."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
    cursor = conn.cursor()
    if Month:
        cursor.execute("SELECT * FROM transactions WHERE Month=? ORDER BY date DESC", (Month,))
    else:
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_spending_by_category(Month=None):
    """Fetches total spending by category for a given Month."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
    cursor = conn.cursor()
    if Month:
        cursor.execute("""
            SELECT category, SUM(abs(amount)) as total,
            count(*) as transaction_count,
            avg(abs(amount)) as average
            FROM transactions
            WHERE amount < 0 AND Month=?
            GROUP BY category
            order by total desc
        """, (Month,))
    else:
        cursor.execute("""
            SELECT category, SUM(abs(amount)) as total,
            count(*) as transaction_count,
            avg(abs(amount)) as average
            FROM transactions
            WHERE amount < 0
            GROUP BY category
            order by total desc
        """)
    rows = cursor.fetchall()
  
    conn.close()
    return [{"category": row["category"], "total": row["total"], "transaction_count": row["transaction_count"], "average": row["average"]} for row in rows]

def get_monthly_summary():
    """Fetches a monthly summary of transactions."""
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
    cursor = conn.cursor()
    cursor.execute("""
    SELECT Month,
    sum(CASE WHEN amount > 0 THEN amount ELSE 0 END) as income,
    sum(CASE WHEN amount < 0 THEN abs(amount) ELSE 0 END) as expenses,
    sum(amount) as net,
    count(*) as transaction_count
    FROM transactions
    GROUP BY Month
    order by Month asc
    """)
    summary = cursor.fetchall()
    print("got summary")
    conn.close()
    return [{"Month": row["Month"], "income": round(row["income"], 2), "expenses": round(row["expenses"], 2), "net": round(row["net"], 2), 
    "transaction_count": row["transaction_count"]} for row in summary]


def save_monthly_summary(summary):
    """Saves or updates monthly summary to the database."""
    # Skip summaries without a valid Month value
    if not summary or not summary.get("Month"):
        print("⚠️ Skipping save: summary has no Month value")
        return False

    conn = get_db_connection()
    cursor = conn.cursor()
    # Upsert by Month: use ON CONFLICT to update existing row for the Month
    cursor.execute("""
    INSERT INTO monthly_summary (Month, income, expenses, net, transaction_count)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(Month) DO UPDATE SET
      income=excluded.income,
      expenses=excluded.expenses,
      net=excluded.net,
      transaction_count=excluded.transaction_count
    """, (summary["Month"], summary["income"], summary["expenses"], summary["net"], summary["transaction_count"]))
    conn.commit()
    conn.close()
    print(f"✓ Monthly summary for {summary['Month']} to database")

if __name__ == "__main__":
    initialize_database()
    get_info()