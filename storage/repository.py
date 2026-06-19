# FileManager는 파일 읽기, 쓰기, 생성만 담당, 
# Repository는 거래 저장, 조회, 삭제, 수정을 담당 -> 차이 구별ß

from models.transaction import Transaction
from storage.file_manager import FileManager
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
    
    def update_amount(self,transaction_id: str, amount: int) -> bool:
        updated = False
        transactions = []
        for transaction in self.iter_transactions():
            if transaction.id == transaction_id:
                transaction.amount = amount
                updated = True
            transactions.append(transaction.to_dict())
        if updated:
            self.file_manager.rewrite_jsonl(transactions)
        return updated