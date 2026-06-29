# 입력 검증
from datetime import datetime

def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError: 
        return False
    
def validate_type(transaction_type: str) -> bool:
    return transaction_type in ["income", "expense"]

def validate_amount(amount) -> bool:
    try:
        amount = int(amount)
        return amount > 0
    except ValueError:
        return False