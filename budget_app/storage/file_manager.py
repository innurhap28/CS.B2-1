from pathlib import Path
import json
from typing import Iterator

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"

class FileManager:
    def __init__(self, data_dir: Path | None = None):
        self.data_dir = data_dir or DATA_DIR

        self.transactions_file = self.data_dir / "transactions.jsonl"
        self.categories_file = self.data_dir / "categories.jsonl"
        self.budgets_file = self.data_dir / "budgets.jsonl"

    def ensure_files(self) -> None:                 # data 파일이 없을 경우 생성
        self.data_dir.mkdir(exist_ok=True)
        self.transactions_file.touch(exist_ok=True)

        if not self.categories_file.exists():
            with self.categories_file.open("w", encoding="utf-8") as file:
                for category in ["food", "transport", "rent", "etc"]:
                    json.dump(category, file, ensure_ascii=False)
                    file.write("\n")

        if not self.budgets_file.exists():
            self.budgets_file.touch()

    def append_jsonl(self, data: dict) -> None:
        with self.transactions_file.open(mode="a", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False)
            file.write("\n")

    def stream_jsonl(self) -> Iterator[dict]:       # 제너레이터 기반 스트리밍 처리
        with self.transactions_file.open(mode="r", encoding="utf-8") as file:
            for line in file:
                yield json.loads(line)

    def rewrite_jsonl(self, transactions: list[dict]) -> None:
        with self.transactions_file.open(mode="w", encoding="utf-8") as file:
            for transaction in transactions:
                json.dump (transaction, file, ensure_ascii=False)
                file.write("\n")

    def read_jsonl(self, file_path: Path, default=None):
        if not file_path.exists():
            return [] if default is None else default

        with file_path.open("r", encoding="utf-8") as file:
            content = file.read().strip()

        if not content:
            return [] if default is None else default

        try:
            parsed = json.loads(content)
            if isinstance(parsed, (dict, list)):
                return parsed
        except json.JSONDecodeError:
            pass

        result = []
        with file_path.open("r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    result.append(json.loads(line))

        if not result:
            return [] if default is None else default
        return result
    
    def write_jsonl(self, file_path: Path, data):
        with file_path.open("w", encoding="utf-8") as file:
            if isinstance(data, dict):
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")
                return

            if isinstance(data, list):
                for item in data:
                    json.dump(item, file, ensure_ascii=False)
                    file.write("\n")
                return

            json.dump(data, file, ensure_ascii=False)
            file.write("\n")