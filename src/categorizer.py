

def categorize_transaction(df, categories):
    """
    Categorize a transaction based on its description.

    Args:
        description (str): Description of the transaction.

    Returns:
        str: Category of the transaction.
    """
    def get_category(description):
        description_lower=description.lower()
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category
        return "Uncategorized" # Default category if no match is found
    
    df["category"] = df["description"].apply(get_category)
    return df
