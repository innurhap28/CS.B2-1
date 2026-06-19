from pathlib import Path
import json
from typing import Iterator

class FileManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)

        self.transactions_file = self.data_dir / "transactions.jsonl"
        self.categories_file = self.data_dir / "categories.json"
        self.budgets_file = self.data_dir / "budgets.json"

    # data 파일이 없을 경우 생성
    def ensure_files(self) -> None:
        self.data_dir.mkdir(exist_ok=True)

        self.transactions_file.touch(exist_ok=True)

        if not self.categories_file.exists():
            self.categories_file.write_text(
                '["food", "transport", "rent", "etc"]',
                encoding="utf-8"
            )

        if not self.budgets_file.exists():
            self.budgets_file.write_text(
                "{}",
                encoding="utf-8"
            )

    # 새로운 거래 데이터를 추가
    def append_jsonl(self, data: dict) -> None:
        with self.transactions_file.open(
            mode="a",
            encoding="utf-8"
        ) as file:
            
            json.dump(data, file, ensure_ascii=False)
            file.write("\n")

    # 제너레이터 기반 스트리밍 처리
    def stream_jsonl(self) -> Iterator[dict]:
        with self.transactions_file.open(
            mode="r",
            encoding="utf-8"
        ) as file:
            
            for line in file:
                yield json.loads(line)

    def rewrite_jsonl(self, transactions: list[dict]) -> None:
        with self.transactions_file.open(mode="w", encoding="utf-8") as file:
            for transaction in transactions:
                json.dump (transaction, file, ensure_ascii=False)
                file.write("\n")
