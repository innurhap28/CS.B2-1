# FileManager는 파일 읽기, 쓰기, 생성만 담당, 
# Repository는 거래 저장, 조회, 삭제, 수정을 담당 -> 차이 구별
# 즉 append_jsonl(data)는 뭘 저장하는지 관심 X
# 하지만 add_transaction(transaction)은 해당 데이터가 거래 데이터임을 확인함?

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