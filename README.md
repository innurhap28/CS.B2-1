# B2-1. 파일 기반 가계부 콘솔 프로그램

```
CS.B2-1/
│
├── main.py                  # 프로그램 시작점, 메뉴 출력
│
├── models/
│   └── transaction.py       # Transaction 클래스
│
├── services/
│   ├── transaction_service.py   # 수입/지출 CRUD
│   ├── category_service.py      # 카테고리 관리
│   └── budget_service.py        # 예산 관리
│
├── storage/
│   └── repository.py        # 파일 입출력(JSON/JSONL)
│   └── file_manager.py
│
│   ├── decorators.py        # 로그, 예외처리 데코레이터
│   └── validators.py        # 입력값 검증
│
├── data/
│   ├── transactions.jsonl   # 거래내역
│   ├── categories.json      # 카테고리 목록
│   └── budgets.json         # 예산 정보
│
└── README.md
```

---
## 1. models/transaction.py

```
from dataclasses import dataclass, field
from typing import List

@dataclass
class Transaction:
    id: str
    date: str
    type: str
    category: str
    amount: int
    memo: str = ""
    tags: List[str] = field(default_factory=list)
```
```
def to_dict(self) -> dict
@classmethod
def from_dict(cls, data: dict)
```

---
## 2. storage/file_manager.py
```
class FileManager:

    def ensure_files(self)

    def read_json(self)

    def write_json(self)

    def append_jsonl(self)

    def stream_jsonl(self)
```
```
def stream_jsonl(self):
    with open(...) as f:
        for line in f:
            yield json.loads(line)
```

---
## 3. storage/repository.py

FileManager는 파일 읽기, 쓰기, 생성만 담당, 
Repository는 거래 저장, 조회, 삭제, 수정을 담당 -> 차이 구별
```
class Repository:

    def add_transaction()

    def get_transaction()

    def iter_transactions()

    def update_transaction()

    def delete_transaction()

    def load_categories()

    def save_categories()

    def load_budgets()

    def save_budgets()
```

---
## 4. services/transaction_service.py
```
class TransactionService:

    def add()

    def list()

    def search()

    def update()

    def delete()

    def export_csv()

    def import_csv()
```

---
## 5. services/category_service.py
```
class CategoryService:

    def add_category()

    def list_categories()

    def remove_category()

    def exists()
```

---
## 6. services/budget_service.py
```
class BudgetService:

    def set_budget()

    def get_budget()

    def calculate_usage()
```

---
## 7. utils/validators.py
```
def validate_date()

def validate_amount()

def validate_type()

def validate_category()
```

---
## 8. utils/decorators.py
```
import time
from functools import wraps
```
실행시간 측정
```
def measure_time(func):
```
예외 처리
```
def handle_error(func):
```
실행 로그
```
def log_action(func):
```
예시
```
@handle_error
@measure_time
def search():
    ...
```

---
## 9. main.py
argparse 사용
```
add
list
search
summary
budget
category
update
delete
import
export
```
10개 명령을 연결

---
### update는 옵션 방식
```
update \
  --id abc123 \
  --amount 30000 \
  --category food
```

---
## 구현 체크리스트

- [x] 대화형 거래 추가 입력 기능
- [x] 거래 목록 출력 기능
- [x] 거래 검색 기능
- [x] 거래 월별 요약 기능
- [x] 예산 설정/조회 기능
- [x] 카테고리 관리 기능
- [x] 거래 수정 기능
- [x] 거래 삭제 기능
- [] 데이터 가져오기/내보내기