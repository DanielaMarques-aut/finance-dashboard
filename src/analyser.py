def summarize_transactions(transactions: list[dict[str, int | float]]):
    """Returns a financial summary dictionary with total income and expenses."""
    income=sum(t["amount"] for t in transactions if t["amount"] > 0)
    expenses=sum(t["amount"] for t in transactions if t["amount"] < 0)
    net=income + expenses
   
   #spending by category
    by_category: dict[int | float, int | float] = {}
    for t in transactions:
        if t["amount"] < 0:  # Only consider expenses for category breakdown
            cat=t["category"]
            if cat not in by_category:
               by_category[cat]=0.0
            by_category[cat]+=abs(t["amount"])
    # Sort categories by spending, highest first
    by_category: dict[str, int | float] = dict(sorted(by_category.items(), key=lambda x: x[1], reverse=True))
    
    return {
        "income": round(income, 2),
        "expenses": round(abs(expenses), 2),
        "net": round(net, 2),
        "by_category": by_category
    }