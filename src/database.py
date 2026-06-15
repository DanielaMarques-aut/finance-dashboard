import sqlite3
import os
from datetime import date
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
            Type TEXT,
            Month TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    #mothly summary table has id, month, income, expenses, net, transaction_count and created_at timestamp
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS monthly_summary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month TEXT NOT NULL UNIQUE,
    income REAL,
    expenses REAL,
    net REAL,
    transaction_count INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully.")

def get_info():
    """Fetches all transactions from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    cursor.execute("""
    SELECT MIN(Date), MAX(Date) FROM transactions
    """)
    date_range = cursor.fetchone()
    conn.close()
    print(f"✓ Database {DB_PATH} contains {count} transactions")
    if date_range[0] and date_range[1]:
        print(f"✓ Transactions date range: {date_range[0]} to {date_range[1]}")
    else:
        print("✓ No transactions found in the database.")

if __name__ == "__main__":
    initialize_database()
    get_info()