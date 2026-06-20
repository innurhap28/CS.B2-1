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

def handle_delete(args):
    print("- 등록된 거래 삭제 ------")
    if not args.id:
        print("삭제할 거래 ID를 입력하세요.")
        return
    deleted = service.delete_transactions(args.id)
    if deleted:
        print("삭제가 완료되었습니다.")
    else:
        print("해당 ID의 거래가 존재하지 않습니다.")

def handle_update(args):
    print("- 등록된 거래 수정 ------")
    if not args.id:
        print("수정할 거래 ID를 입력하세요.")
        return
    updated = service.update_transactions(
        transaction_id=args.id,
        date=args.date,
        transaction_type=args.type,
        category=args.category,
        amount=args.amount
    )
    if updated:
        print("수정 완료!")
    else:
        print("해당 ID의 거래가 존재하지 않습니다.")

def handle_category(args):
    if args.action == "list":
        categories = service.get_categories()
        print("- 카테고리 목록 ----------")
        for category in categories:
            print(category)
    elif args.action == "add":
        if not args.value:
            print("추가할 카테고리를 입력하세요.")
            return
        if service.add_category(args.value):
            print("카테고리 추가 완료!")
        else:
            print("이미 존재하는 카테고리입니다.")
    elif args.action == "remove":
        if not args.value:
            print("삭제할 카테고리를 입력하세요.")
            return
        if service.remove_category(args.value):
            print("카테고리 삭제 완료!")
        else:
            print("삭제할 수 없습니다.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["add", "list", "search", "summary", "delete", "update", "category"])
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--from-date")
    parser.add_argument("--to-date")
    parser.add_argument("--category")
    parser.add_argument("--type")
    parser.add_argument("--month", default=None)
    parser.add_argument("--id")
    parser.add_argument("--amount", type=int)
    parser.add_argument("--date")
    parser.add_argument("action", nargs="?")
    parser.add_argument("value", nargs="?")
    args = parser.parse_args()
    if args.command == "add":
        handle_add()
    elif args.command == "list":
        handle_list(args)
    elif args.command == "search":
        handle_search(args)
    elif args.command == "summary":
        handle_summary(args)
    elif args.command == "delete":
        handle_delete(args)
    elif args.command == "update":
        handle_update(args)
    elif args.command == "category":
        handle_category(args)

if __name__ == "__main__":
    main()