# 프로그램 진입점
import argparse, uuid
from services.transaction_service import TransactionService
from models.transaction import Transaction
from utils.validators import validate_amount, validate_date, validate_type

parser = argparse.ArgumentParser()

parser.add_argument("command", choices=["add", "list", "search", "delete"])

args = parser.parse_args()

service = TransactionService()

if args.command == "add":
    print("- 거래 추가 -----")
    date = input("날짜: ")
    if not validate_date(date):
        print("날짜 형식이 올바르지 않습니다.")
        exit(1)
    transaction_type = input("타입: ")
    if not validate_type(transaction_type):
        print("거래 타입은 income/expense 중에서 입력하세요.")
        exit(1)
    category = input("카테고리: ")
    amount = input("금액: ")
    if not validate_amount(amount):
        print("금액이 올바르지 않습니다.")
        exit(1)
    transaction = Transaction(
        id=uuid.uuid4().hex[:8], date=date, type=transaction_type, category=category, amount=int(amount)
    )
    service.add_transaction(transaction)
    print(f"저장이 완료되었습니다. ID : {transaction.id}")

elif args.command == "list":
    print("- 거래 목록 -----")