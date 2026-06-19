# 거래 관련 기능 담당
from storage.repository import Repository
from typing import Iterator
from models.transaction import Transaction

class TransactionService:
    def __init__(self):
        self.repository = Repository()

    def list_transactions(self) -> Iterator[Transaction]:
        yield from self.repository.iter_transactions()

    def add_transaction(self, transaction: Transaction) -> None:
        self.repository.add_transaction(transaction)