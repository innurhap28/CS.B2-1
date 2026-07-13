from ..utils.decorators import handle_error
from ..storage.repository import Repository
from ..models.transaction import Transaction
import csv, uuid

class CsvService:
    def __init__(self):
        self.repository = Repository()

    @handle_error
    def export_csv(
            self, output_file: str, 
            month: str | None = None,
            from_date: str | None = None,
            to_date: str | None = None
    ):
        count = 0
        with open(output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["date", "type", "category", "amount", "memo", "tags"])
            for tx in self.repository.iter_transactions():
                if month:
                    if not tx.date.startswith(month):
                        continue
                elif from_date and to_date:
                    if not (from_date <= tx.date <= to_date):
                        continue
                writer.writerow([tx.date, tx.type, tx.category, tx.amount, tx.memo, ",".join(tx.tags)])
                count += 1
        return count
    
    @handle_error
    def import_csv(self, csv_file: str):
        count = 0
        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["category"] not in self.repository.get_categories():
                    continue
                tx = Transaction(
                    id=str(uuid.uuid4())[:8],
                    date=row["date"], type=row["type"], category=row["category"], 
                    amount=int(row["amount"]), memo=row["memo"], tags=row["tags"].split(",")
                    if row["tags"]
                    else []
                )
                self.repository.add_transaction(tx)
                count += 1
        return count