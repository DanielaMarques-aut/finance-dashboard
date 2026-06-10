from openpyxl import load_workbook
from datetime import date
import pandas as pd
import os

def fill_Template(summary, df, output_path):
    """Fills the Excel template with summary and transaction data."""
    # Load the template
   
    wb = load_workbook("Data/Finance_template.xlsx")
  
    # Fill Dashboard sheet
    ws_dashboard = wb["Dashboard"]
    moth_label=date.today().strftime("%B %Y")
    ws_dashboard["B2"] = moth_label
    ws_dashboard["B3"] = date.today().strftime("%B %d, %Y")
    ws_dashboard["B7"] = round(summary["income"], 2)
    ws_dashboard["B8"] = round(summary["expenses"], 2)
    ws_dashboard["B9"] = round(summary["net"], 2)

    
    # Fill Transactions sheet
    ws_trans = wb["Transactions"]
    df_export = df[["date", "description", "amount", "category"]].copy()
    df_export["date"] = df_export["date"].dt.strftime("%Y-%m-%d")
    for r_idx, row in enumerate(df_export.values, start=2):
        ws_trans[f"A{r_idx}"] = row[0]
        ws_trans[f"B{r_idx}"] = row[1]
        ws_trans[f"C{r_idx}"] = row[2]
        ws_trans[f"D{r_idx}"] = row[3]

# Fill Categories sheet
    ws_cats = wb["Categories"]
    for r_idx, (cat, amount) in enumerate(summary["by_category"].items(), start=2):
        ws_cats[f"A{r_idx}"] = cat
        ws_cats[f"B{r_idx}"] = round(amount, 2)
    
#save the filled template as a new file
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    print(f"✓ Excel report generated at {output_path}")