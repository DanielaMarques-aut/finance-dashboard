from datetime import date

def print_report(summary):
   print("\n" + "=" * 45)
   print("   MONTHLY FINANCE REPORT")
   print(f"   Generated on: {date.today()}")
   print("=" * 45)

   print(f"{'Income:':.<30}+{summary['income']:.2f}€")
   print(f"{'Expenses:':.<30}-{summary['expenses']:.2f}€")
   print(f"{'Net:':.<30}{summary['net']:.2f}€")

   print("\nSpending by Category:")
   for category, amount in summary["by_category"].items():
         print(f"  {category:<25} {amount:.2f}€")
         bar = "█" * int(amount / 10)   # visual bar
         print(f"{category:.<20} {amount:>8.2f}€  {bar}")
    
   print("=" * 45)

def save_report(summary, filepath):
    """Saves the report to a text file."""
    with open(filepath, "w") as f:
        f.write("MONTHLY FINANCE REPORT\n")
        f.write(f"Generated: {date.today()}\n\n")
        f.write(f"Income:   {summary['income']:.2f}€\n")
        f.write(f"Expenses: {summary['expenses']:.2f}€\n")
        f.write(f"Net:      {summary['net']:.2f}€\n\n")
        f.write("Spending by Category:\n")
        for category, amount in summary["by_category"].items():
            f.write(f"  {category}: {amount:.2f}€\n")
    
    print(f"\n✓ Report saved to {filepath}")