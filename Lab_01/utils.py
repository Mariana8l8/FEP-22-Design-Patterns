def check_amount(amount: float) -> bool:
    if amount < 0:
        print(f"[Error] Provided value {amount} is below zero. Please enter a positive number.")
        return True
    return False
