# 파일 기반 가계부 콘솔 프로그램

## 1. 프로젝트 소개

Python 기반의 파일 저장형(Console) 가계부 프로그램입니다.

거래 내역을 추가, 조회, 수정, 삭제할 수 있으며, 검색, 월별 요약, 카테고리 관리, 예산 관리, CSV 가져오기/내보내기 기능을 제공합니다.

데이터는 프로그램 종료 후에도 유지되도록 파일에 저장되며, 거래 내역 조회 및 검색 시 제너레이터(yield)를 이용한 스트리밍 방식을 사용합니다.

또한 데코레이터를 활용하여 공통 기능(예외 처리, 실행 시간 측정)을 분리하였습니다.

---

## 2. 프로젝트 구조

```text
CS.B2-1/
│
├── main.py                  # 프로그램 시작점, 메뉴 출력
│
├── messages.json            # 출력 메시지 상수 분리
│
├── models/
│   └── transaction.py       # Transaction 클래스
│
├── services/
│   ├── transaction_service.py   # 수입/지출 CRUD
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

## 3. 저장 파일

### transactions.jsonl

거래 내역 저장 파일

예시

```json
{
  "id": "a1b2c3d4",
  "date": "2026-06-22",
  "type": "expense",
  "category": "food",
  "amount": 12000,
  "memo": "점심 식사",
  "tags": ["meal", "lunch"]
}
```

---

### categories.json

카테고리 목록 저장

예시

```json
[
  "food",
  "transport",
  "shopping",
  "salary"
]
```

---

### budgets.json

월별 예산 저장

예시

```json
{
  "2026-06": 500000,
  "2026-07": 600000
}
```

---

## 4. 실행 방법

### 거래 추가

```bash
python main.py add
```

---

### 거래 목록 조회

```bash
python main.py list

python main.py list --limit 20
```

---

### 거래 검색

```bash
python main.py search --category food

python main.py search --type expense

python main.py search --from-date 2026-06-01 --to-date 2026-06-30

python main.py search --tag lunch
```

---

### 월별 요약

```bash
python main.py summary --month 2026-06
```

---

### 예산 설정

```bash
python main.py budget set --month 2026-06 --amount 500000
```

---

### 예산 조회

```bash
python main.py budget get --month 2026-06
```

---

### 카테고리 추가

```bash
python main.py category add food
```

---

### 카테고리 목록 조회

```bash
python main.py category list
```

---

### 카테고리 삭제

```bash
python main.py category remove food
```

---

### 거래 수정

```bash
python main.py update \
  --id abc123 \
  --amount 30000 \
  --category food
```

---

### 거래 삭제

```bash
python main.py delete --id abc123
```

---

### CSV 내보내기

```bash
python main.py export \
  --out output.csv \
  --month 2026-06
```

---

### CSV 가져오기

```bash
python main.py import \
  --from transactions.csv
```

---

## 5. CSV 스키마

가져오기(import)와 내보내기(export)는 아래 형식을 사용합니다.

| column   | required | 설명               |
| -------- | -------- | ---------------- |
| date     | Y        | YYYY-MM-DD       |
| type     | Y        | income / expense |
| category | Y        | 등록된 카테고리         |
| amount   | Y        | 양수 정수            |
| memo     | N        | 메모               |
| tags     | N        | 쉼표(,) 구분 문자열     |

예시

```csv
date,type,category,amount,memo,tags
2026-06-22,expense,food,12000,점심,lunch,meal
2026-06-25,income,salary,3000000,월급,payday
```

---

## 6. 주요 기능

* 거래 추가(Add)
* 거래 목록 조회(List)
* 거래 검색(Search)
* 거래 수정(Update)
* 거래 삭제(Delete)
* 월별 요약(Summary)
* 예산 설정 및 조회(Budget)
* 카테고리 관리(Category)
* CSV 가져오기(Import)
* CSV 내보내기(Export)

---

## 7. 구현 특징

### 제너레이터 기반 스트리밍

거래 내역 조회 및 검색 시 JSONL 파일 전체를 메모리에 올리지 않고 한 줄씩 읽어 처리합니다.

```python
def stream_jsonl(self):
    with open(self.transactions_file, encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)
```

---

### 데코레이터 활용

공통 기능을 데코레이터로 분리하였습니다.

* 예외 처리
* 실행 시간 측정

예시

```python
@handle_error
@measure_time
def search():
    ...
```

---

### 타입 힌트 적용

함수의 입력값과 반환값을 명확하게 표현하여 가독성과 유지보수성을 향상시켰습니다.

```python
def get_transaction(self, transaction_id: str) -> Transaction | None:
    ...
```

---

## 8. 개발 환경

* Python 3.11+
* argparse
* json
* csv
* pathlib
* dataclasses
* typing
* uuid
