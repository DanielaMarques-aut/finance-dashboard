# Category rules: keyword → category
# Order matters - first match wins
categories:dict[str,list[str]]= {
    "Groceries":     ["continente", "pingo doce", "lidl", "aldi", "mercadona", "minipreco"],
    "Utilities":     ["edp", "nos ", "vodafone", "meo ", "galp", "aguas", "gas"],
    "Transport":     ["uber", "bolt", "cp ", "metro", "carris", "galp combusti"],
    "Streaming":     ["netflix", "spotify", "youtube", "disney", "hbo"],
    "Health":        ["farmacia", "clinica", "hospital", "dentista", "saude"],
    "Food & Dining": ["restaurante", "tasca", "cafe", "mcdonald", "pizza"],
    "Shopping":      ["worten", "fnac", "zara", "primark", "amazon"],
    "Income":        ["salario", "ordenado", "mb way recebido", "transferencia recebida"],
    "Transfers":     ["mb way", "transferencia"],
}

def categorize_transaction(description: str) -> str:
    """
    Categorize a transaction based on its description.

    Args:
        description (str): Description of the transaction.

    Returns:
        str: Category of the transaction.
    """
    description_lower: str=description.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in description_lower:
                return category
    return "Uncategorized" # Default category if no match is found
def categorize_all_transactions(transactions: list[dict[str, str]]):
    """
    Categorize a list of transactions.

    Args:
        transactions (list): List of transaction dictionaries.

    Returns:
        list: List of categorized transaction dictionaries.
    """
    for transaction in transactions:
        transaction["category"] = categorize_transaction(description=transaction["description"])
    return transactions