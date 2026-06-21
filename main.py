# 프로그램 진입점
import argparse, uuid, json, os
from services.transaction_service import TransactionService
from models.transaction import Transaction
from utils.validators import (validate_amount, validate_date, validate_type)
from services.budget_service import BudgetService

service = TransactionService()
budget_service = BudgetService()

def load_messages(lang="ko"):
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path, "messages.json")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(lang, data["ko"])

msg = load_messages(lang="ko")

def get_valid_input(prompt, validator, error_message): 
    while True:
        value = input(prompt)
        if validator(value):
            return value
        print(error_message)

def handle_add(args):
    print(msg["MENU_add"])
    date = get_valid_input("날짜 : ", validate_date, msg["ERR_not_valid_date"])
    transaction_type = get_valid_input("타입 : ", validate_type, msg["ERR_not_valid_type"])
    category = input("카테고리 : ")
    amount = int(get_valid_input("금액 : ", validate_amount, msg["ERR_not_valid_amount"]))
    transaction = Transaction(id=uuid.uuid4().hex[:8], date = date, type = transaction_type, category=category, amount=int(amount))
    service.add_transaction(transaction)
    print(f"저장 완료. ID = {transaction.id}")

def handle_list(args):
    print(msg["MENU_list"])
    transactions = service.list_transactions(limit=args.limit)
    for tx in transactions:
        print(f"{tx.id} | {tx.date} | {tx.type} | {tx.category} | {tx.amount}")

def handle_search(args):
    print(msg["MENU_search"])
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
        print(msg["no_result"])

def handle_summary(args):
    print(msg["MENU_summary"])
    result = service.get_monthly_summary(args.month)
    if result is None:
        print(msg["no_data"])
        return
    print(f"총 수입 : {result['income']}\n총 지출 : {result['expense']}\n잔액 : {result['balance']}")
    print(f"\n카테고리별 지출 TOP {args.top}")
    for category, amount in result["top_categories"][:args.top]:
        print(f"{category}: {amount:,}원")
    budget = budget_service.get_budget(args.month)
    if budget is not None:
        usage = result['expense'] / budget * 100
        print(f"\n예산: {budget:,}원")
        print(f"사용률: {usage:.1f}%")
        if result['expense'] > budget:
            print(msg["exceed_budget"])


def handle_delete(args):
    print(msg["MENU_delete"])
    if not args.id:
        print(msg["ID_to_delete"])
        return
    deleted = service.delete_transactions(args.id)
    if deleted:
        print(msg["complete_delete"])
    else:
        print(msg["ERR_not_found_id"])

def handle_update(args):
    print(msg["MENU_update"])
    if not args.id:
        print(msg["ID_to_update"])
        return
    updated = service.update_transactions(
        transaction_id=args.id,
        date=args.date,
        transaction_type=args.type,
        category=args.category,
        amount=args.amount
    )
    if updated:
        print(msg["complete_update"])
    else:
        print(msg["ERR_not_found_id"])

def handle_category(args):
    if args.action == "list":
        categories = service.get_categories()
        print(msg["MENU_category"])
        for category in categories:
            print(category)
    elif args.action == "add":
        if not args.value:
            print(msg["CATE_to_add"])
            return
        if service.add_category(args.value):
            print(msg["complete_add"])
        else:
            print(msg["existing_cate"])
    elif args.action == "remove":
        if not args.value:
            print(msg["CATE_to_delete"])
            return
        if service.remove_category(args.value):
            print(msg["complete_delete"])
        else:
            print(msg["cannot_delete"])

def handle_budget(args):
    if args.budget_action == "set":
        budget_service.set_budget(args.month, args.amount)
        print(f"{args.month} 예산 {args.amount:,}원 저장 완료")

def handle_export(args):
    if not args.month and not (args.from_date and args.to_date):
        print("--month 또는 --from-date/--to-date 조건이 필요합니다.")
        exit(1)
    count = service.export_csv(args.out, args.month, args.from_date, args.to_date)
    print(f"{count}건을 {args.out}에 저장했습니다.")

def handle_import(args):
    count = service.import_csv(args.from_file)
    print(f"{count}건을 가져왔습니다.")

def create_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("add")
    list_parser = subparsers.add_parser("list")
    list_parser.add_argument("--limit", type=int, default=10)
    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("--from-date")
    search_parser.add_argument("--to-date")
    search_parser.add_argument("--category")
    search_parser.add_argument("--type")
    summary_parser = subparsers.add_parser("summary")
    summary_parser.add_argument("--month", required=True)
    summary_parser.add_argument("--top", type=int, default=5)
    budget_parser = subparsers.add_parser("budget")
    budget_subparsers = budget_parser.add_subparsers(dest="budget_action", required=True)
    budget_set_parser = budget_subparsers.add_parser("set")
    budget_set_parser.add_argument("--month", required=True)
    budget_set_parser.add_argument("--amount", type=int, required=True)
    delete_parser = subparsers.add_parser("delete")
    delete_parser.add_argument("--id", required=True)
    update_parser = subparsers.add_parser("update")
    update_parser.add_argument("--id", required=True)
    update_parser.add_argument("--amount", type=int)
    update_parser.add_argument("--date")
    update_parser.add_argument("--category")
    update_parser.add_argument("--type")
    category_parser = subparsers.add_parser("category")
    category_parser.add_argument("action", choices=["add", "list", "remove"])
    category_parser.add_argument("value", nargs="?")
    export_parser = subparsers.add_parser("export")
    export_parser.add_argument("--out", required=True)
    export_parser.add_argument("--month")
    export_parser.add_argument("--from-date")
    export_parser.add_argument("--to-date")
    import_parser = subparsers.add_parser("import")
    import_parser.add_argument("--from-file", required=True)
    return parser

def main():
    args = create_parser().parse_args()
    handlers = {
        "add": handle_add,
        "list": handle_list,
        "search": handle_search,
        "summary": handle_summary,
        "delete": handle_delete,
        "update": handle_update,
        "category": handle_category,
        "budget": handle_budget,
        "import": handle_import,
        "export": handle_export
    }
    handlers[args.command](args)

if __name__ == "__main__":
    main()