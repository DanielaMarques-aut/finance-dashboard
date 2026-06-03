def summarise(df):
    """Returns a financial summary using pandas."""
    
    expenses_df = df[df["amount"] < 0].copy()
    income_df = df[df["amount"] > 0].copy()
    total=expenses_df.merge(income_df, how="outer", on=["date", "description", "amount", "type"], indicator=True)## VLOOKUP equivalent — merge two DataFrames
    print(total)
    total_income = income_df["amount"].sum() #sum if excel function 
    total_expenses = expenses_df["amount"].sum()
    net = total_income + total_expenses
    
    # Spending by category using groupby
    by_category = (
        expenses_df
        .groupby("category")["amount"]
        .sum()
        .abs()                          # make positive
        .sort_values(ascending=False)   # highest first
        .round(2)
    )
    
    # COUNTIF equivalent
    count_debits = len(df[df["type"] == "debit"])
    print(f"Debit count (COUNTIF type=debit): {count_debits}")
    # Most expensive single transaction
    biggest = expenses_df.loc[expenses_df["amount"].idxmin()]
    # AVERAGEIF equivalent
    avg_expense = df[df["amount"] < 0]["amount"].mean()
    print(f"Average expense (AVERAGEIF): {abs(avg_expense):.2f}€")
    
    return {
        "income": round(total_income, 2),
        "expenses": round(abs(total_expenses), 2),
        "net": round(net, 2),
        "by_category": by_category.to_dict(),
        "biggest_expense": {
            "description": biggest["description"],
            "amount": abs(biggest["amount"])
        },
        "transaction_count": len(df)
    }