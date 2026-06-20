# 프로그램 진입점
import argparse, uuid
from services.transaction_service import TransactionService
from models.transaction import Transaction
from utils.validators import (validate_amount, validate_date, validate_type)

service = TransactionService()

def get_valid_input(prompt, validator, error_message): 
    while True:
        value = input(prompt)
        if validator(value):
            return value
        print(error_message)

def handle_add():
    print("- 거래 추가 ----------")
    date = get_valid_input("날짜 : ", validate_date, "날짜 형식이 올바르지 않습니다.")
    transaction_type = get_valid_input("타입 : ", validate_type, "income 또는 expense만 입력 가능합니다.")
    category = input("카테고리 : ")
    amount = int(get_valid_input("금액 : ", validate_amount, "양의 정수를 입력하세요."))
    transaction = Transaction(id=uuid.uuid4().hex[:8], date = date, type = transaction_type, category=category, amount=int(amount))
    service.add_transaction(transaction)
    print(f"저장 완료. ID = {transaction.id}")

def handle_list(args):
    print("- 거래 목록 ----------")
    transactions = service.list_transactions(limit=args.limit)
    for tx in transactions:
        print(f"{tx.id} | {tx.date} | {tx.type} | {tx.category} | {tx.amount}")

def handle_search(args):
    print("- 거래 검색 ----------")
    transactions = service.search_transactions(
        from_date=args.from_date,
        to_date=args.to_date,
        category=args.category,
        transaction_type=args.type
    )
    found = False
    for tx in transactions:
        found = True
        print(f"{tx.id} | {tx.date} | {tx.type} | {tx.category} | {tx.amount}")
    if not found: 
        print("검색 결과가 없습니다.")

def handle_summary(args):
    print("- 월별 요약 ----------")
    result = service.get_monthly_summary(args.month)
    print(f"총 수입 : {result['income']}\n총 지출 : {result['expense']}\n잔액 : {result['balance']}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["add", "list", "search", "summary", "delete"])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--from-date")
    parser.add_argument("--to-date")
    parser.add_argument("--category")
    parser.add_argument("--type")
    parser.add_argument("--month", default=None)
    args = parser.parse_args()
    if args.command == "add":
        handle_add()
    elif args.command == "list":
        handle_list(args)
    elif args.command == "search":
        handle_search(args)
    elif args.command == "summary":
        handle_summary(args)

if __name__ == "__main__":
    main()