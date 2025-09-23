def check_amount(amount: float) -> bool:
    if amount < 0:
        print(f"Invalid usage amount: {amount}. Must be a positive value.")
        return True
    return False
