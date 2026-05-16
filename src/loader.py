import os
from pathlib import Path

def load_transactions(file_path: Path | str) :
    """
    Load transactions from a CSV file.

    Args:
        file_path (Path): Path to the transactions CSV file.

    Returns:
        list: List of transactions dictionaries.
    """
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        raise FileNotFoundError(f"File not found: {file_path}")

    transactions: list[dict[str, str | int | float]] = []
    with open(file_path, "r") as f:
        # Skip the header line
        f.readline()
        for LINE_NUMBER, line in enumerate(f, start=2):   
            Parts: list[str]=line.strip().split(",")
            # Parse each line and create a transaction dictionary
            try:   
                transaction: dict[str, str | int | float] ={
                    "date": Parts[0],
                    "description": Parts[1],
                    "amount": float(Parts[2]),
                    "type": Parts[3]
                }
                transactions.append(transaction)
            except(ValueError, IndexError) as e:
                 print(f"❌ Error parsing line {LINE_NUMBER}: {e}")
                 
            except Exception as e:
                 print(f"❌ Error parsing line {LINE_NUMBER}: {e}")
    print(f"✓ Loaded {len(transactions)} transactions from {file_path}")             

    return transactions