from ..models.transaction import Transaction
from .file_manager import FileManager
from typing import Iterator

class Repository:
    def __init__(self):
        self.file_manager = FileManager()
        self.file_manager.ensure_files()

    def add_transaction(self, transaction: Transaction) -> None:
        self.file_manager.append_jsonl(transaction.to_dict())
    
    def iter_transactions(self) -> Iterator[Transaction]:
        for data in self.file_manager.stream_jsonl():
            yield Transaction.from_dict(data)

    def find_by_id(self, transaction_id: str) -> Transaction | None:
        for transaction in self.iter_transactions():
            if transaction.id == transaction_id:
                return transaction
        return None
    
    def delete_transaction(self, transaction_id: str) -> bool:
        remaining_transactions=[]
        deleted = False
        for transaction in self.iter_transactions():
            if transaction.id == transaction_id:
                deleted = True
                continue
            remaining_transactions.append(transaction.to_dict())
        if deleted:
            self.file_manager.rewrite_jsonl(remaining_transactions)
        return deleted
    
    def update_transaction(self, transaction_id: str, date=None, transaction_type=None, category=None, amount=None, memo=None, tags=None) -> bool:
        updated = False
        transactions = []
        for transaction in self.iter_transactions():
            if transaction.id == transaction_id:
                if date is not None:
                    transaction.date = date
                if transaction_type is not None:
                    transaction.type = transaction_type
                if category is not None:
                    transaction.category = category
                if amount is not None:
                    transaction.amount = amount
                if memo is not None:
                    transaction.memo = memo
                if tags is not None:
                    transaction.tags = tags
                updated = True
            transactions.append(transaction.to_dict())
        if updated:
            self.file_manager.rewrite_jsonl(transactions)
        return updated
    
    def get_categories(self) -> list[str]:
        return self.file_manager.read_json(self.file_manager.categories_file)

    def add_category(self, category: str) -> bool:
        categories = self.file_manager.read_json(self.file_manager.categories_file)
        if category in categories:
            return False
        categories.append(category)
        self.file_manager.write_json(self.file_manager.categories_file, categories)
        return True

    def remove_category(self, category):
        categories = self.file_manager.read_json(self.file_manager.categories_file)
        if category not in categories:
            return False
        categories.remove(category)
        self.file_manager.write_json(self.file_manager.categories_file, categories)
        return True
    
    def load_budgets(self) -> dict:
        return self.file_manager.read_json(self.file_manager.budgets_file)
    
    def save_budgets(self, budgets: dict) -> None:
        self.file_manager.write_json(self.file_manager.budgets_file, budgets)
