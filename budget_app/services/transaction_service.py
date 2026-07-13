# 거래 관련 기능 담당
from ..storage.repository import Repository
from typing import Iterator
from ..models.transaction import Transaction
from ..utils.decorators import handle_error

class TransactionService:
    def __init__(self):
        self.repository = Repository()

    def add_transaction(self, transaction: Transaction) -> None:
        self.repository.add_transaction(transaction)

    def list_transactions(self, limit=None) -> Iterator[Transaction]:
        count = 0
        transactions = list(self.repository.iter_transactions())
        for tx in reversed(transactions):
            yield tx
            count += 1
            if limit and count >= limit:
                break
    
    def search_transactions(self, from_date=None, to_date=None, category=None, transaction_type=None, q=None, tag=None):
        results = []
        for tx in self.repository.iter_transactions():
            if from_date and tx.date < from_date:
                continue
            if to_date and tx.date > to_date:
                continue
            if category and tx.category != category:
                continue
            if transaction_type and tx.type != transaction_type:
                continue
            if q and q.lower() not in tx.memo.lower():
                continue
            if tag and tag not in tx.tags:
                continue
            results.append(tx)
        yield from reversed(results)
    
    def get_monthly_summary(self, month=None):
        income = 0
        expense = 0
        category_expense = {}
        for tx in self.repository.iter_transactions():
            if not tx.date.startswith(month):
                continue
            if tx.type == "income":
                income += tx.amount
            elif tx.type == "expense":
                expense += tx.amount
                category_expense[tx.category] = (category_expense.get(tx.category, 0) + tx.amount)
        top_categories = sorted(category_expense.items(), key=lambda x: x[1], reverse=True)
        if income == 0 and expense == 0:
            return None
        return {"income": income, "expense": expense, "balance": income - expense, "top_categories": top_categories}
    
    @handle_error
    def delete_transactions(self, transaction_id: str) -> bool:
        return self.repository.delete_transaction(transaction_id)

    def update_transactions(self, transaction_id, date, transaction_type, category, amount, memo, tags):
        return self.repository.update_transaction(transaction_id, date, transaction_type, category, amount)

    def get_categories(self):
        return self.repository.get_categories()
    
    def add_category(self, category):
        return self.repository.add_category(category)

    def remove_category(self, category: str) -> bool:
        for tx in self.repository.iter_transactions():
            if tx.category == category:
                return False
        return self.repository.remove_category(category)