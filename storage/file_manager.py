from pathlib import Path

class FileManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)

        self.transactions_file = self.data_dir / "transactions.jsonl"
        self.categories_file = self.data_dir / "categories.json"
        self.budgets_file = self.data_dir / "budgets.json"

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
