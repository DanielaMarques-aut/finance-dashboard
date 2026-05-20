from datetime import date
from matplotlib import pyplot as plt
import pandas as pd

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
    categories=summary["by_category"]
    if not categories:
        print("\nNo categories found in summary. Skipping report generation.")
        return
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

def save_chart(summary, filepath):
    categories = summary["by_category"]
    if not categories:
        print("\nNo categories found in summary. Skipping chart generation.")
        return
    #create a figure with 2 subplots:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    # Bar chart — spending by category
    pd.Series(categories).plot(kind="bar", ax=ax1, color="skyblue", edgecolor="black")
    ax1.set_title("Spending by Category")
    ax1.set_xlabel("Category")
    ax1.set_ylabel("Amount (€)")
    ax1.grid(axis="y", linestyle="--", alpha=0.7)
    ax1.tick_params(axis="x", rotation=45)
    # Pie chart — porporcion of spending by category
    pd.Series(categories).plot(kind="pie", ax=ax2, autopct="%1.1f%%", startangle=90)
    ax2.set_title("Spending Distribution")
    ax2.set_ylabel("")  # Hide y-label for pie chart
    plt.suptitle(f"Monthly Finance Report - {date.today()}", fontsize=10, fontweight="bold")
    plt.tight_layout()
    plt.savefig(filepath, format="png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()
    print(f"✓ Chart saved to {filepath}")