from pandas.core.frame import DataFrame
import os
from pathlib import Path
import pandas as pd

def load_transactions(file_path: Path | str) :
    """
    Load transactions from a CSV file, using pandas for efficient data handling. 
    Each transaction is represented as a dictionary with keys: date, description, amount, and type.

    Args:
        file_path (Path): Path to the transactions CSV file.

    Returns:
        dataframe: A pandas DataFrame containing the transactions.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df: DataFrame=pd.read_csv(file_path)
    # Convert date column to actual dates (not strings)
    df["date"]=pd.to_datetime(df["date"], errors="coerce")

     # Strip whitespace from text columns
    df["description"]=df["description"].str.strip()
    df["type"]=df["type"].str.strip()
    
    print(f"✓ Loaded {len(df)} transactions from {file_path}")
    print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
    print(f"Columns: {list(df.columns)}")
       

    return df
    