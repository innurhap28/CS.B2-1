# 거래 데이터 구조 정의

from dataclasses import dataclass, field

@dataclass
class Transaction:
    id: str
    date: str
    type: str
    category: str
    amount: int
    memo: str = ""
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date,
            "type": self.type,
            "category": self.category,
            "amount": self.amount,
            "memo": self. memo,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            date=data["date"],
            type=data["type"],
            category=data["category"],
            amount=data["amount"],
            memo=data["memo"],
            tags=data["tags"]
        )