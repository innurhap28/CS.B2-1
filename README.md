# 파일 기반 가계부 콘솔 프로그램

## 1. 프로젝트 소개

Python 기반의 파일 저장형(Console) 가계부 프로그램

거래 내역을 추가/조회/수정/삭제할 수 있으며, 검색/월별 요약/카테고리 관리/예산 관리/CSV 가져오기 및 내보내기 기능을 제공한다.

데이터는 프로그램 종료 후에도 유지되도록 파일에 저장되며, 거래 내역 조회 및 검색 시 제너레이터(yield)를 이용한 스트리밍 방식을 사용한다.

또한 데코레이터를 활용하여 공통 기능(예외 처리, 실행 로그)을 분리하였다.

---

## 2. 프로젝트 구조

```text
CS.B2-1/
├── budget_app/
│   ├── __init__.py
│   ├── __main__.py
│   ├── messages.py
│   │
│   ├── models/
│   │   └── transaction.py
│   │
│   ├── services/
│   │   ├── transaction_service.py
│   │   ├── csv_service.py
│   │   └── budget_service.py
│   │
│   ├── storage/
│   │   ├── file_manager.py
│   │   └── repository.py
│   │
│   ├── utils/
│   │   ├── decorators.py
│   │   ├── logger.py
│   │   └── validators.py
│   │
│   │
│   └── logs/
│       └── command.log
│
├── data/
│   ├── transactions.jsonl
│   ├── categories.jsonl
│   └── budgets.jsonl
│
└── README.md
```

---

## 3. 주요 기능 및 실행 방법

### 거래 추가

```bash
python -m budget_app add
```

- 대화형 입력을 통해 거래에 대한 정보를 등록하여 새로운 거래 내역을 추가하는 기능. 

카테고리와 입력 값을 검증한 후, 8글자의 거래 ID를 생성하여 `transactions.jsonl`에 저장한다.


---

### 거래 목록 조회

```bash
python -m budget_app list

python -m budget_app list --limit 20
```

- 저장된 거래 내역을 최신 순으로 조회하는 기능. 

제너레이터를 이용하여 파일을 한 줄씩 읽어내어, 메모리를 효율적으로 사용하는 방법을 채택하였다. 
`--limit {int}` 옵션을 사용하여 최신 N개의 거래 내역만 조회 가능하다. 

---

### 거래 검색

```bash
python -m budget_app search --category food

python -m budget_app search --type expense

python -m budget_app search --from-date 2026-06-01 --to-date 2026-06-30

python -m budget_app search --tag lunch
```

* 기간, 카테고리, 거래 유형, 태그 등의 조건을 이용하여 원하는 거래 내역을 검색하는 기능.

검색 결과는 최신 순으로 출력되며, 제너레이터를 이용한 스트리밍 방식으로 처리하여 메모리 사용량을 최소화하였다.

---

### 월별 요약

```bash
python -m budget_app summary --month 2026-06
```

* 특정 월의 총수입, 총지출, 잔액 및 카테고리별 지출 내역을 요약하여 출력하는 기능.

해당 월의 예산이 설정되어 있는 경우 예산 사용률과 예산 초과 여부도 함께 확인할 수 있다.

---

### 예산 설정

```bash
python -m budget_app budget set --month 2026-06 --amount 500000
```

* 지정한 월의 예산을 설정하거나 기존 예산을 변경하는 기능.

설정한 예산은 `budgets.json`에 저장되며, 월별 요약 기능에서 예산 사용 현황을 계산하는 기준으로 사용된다.

---

### 예산 조회

```bash
python -m budget_app budget get --month 2026-06
```

* 특정 월에 설정된 예산을 조회하는 기능.

설정된 예산이 없는 경우에는 안내 메시지를 출력하며, 등록된 예산이 있을 경우 해당 금액을 출력한다.

---

### 카테고리 추가

```bash
python -m budget_app category add food
```

* 새로운 카테고리를 등록하는 기능.

이미 존재하는 카테고리는 중복 등록되지 않으며, 등록이 완료되면 `categories.json`에 즉시 반영된다.

---

### 카테고리 목록 조회

```bash
python -m budget_app category list
```

- 현재 등록되어 있는 모든 카테고리를 조회하는 기능.

거래 등록 시 사용할 수 있는 카테고리 목록을 한 번에 확인할 수 있다.

---

### 카테고리 삭제

```bash
python -m budget_app category remove food
```

- 등록된 카테고리를 삭제하는 기능.

해당 카테고리를 사용하는 거래 내역이 존재하는 경우 삭제를 제한하여 데이터의 일관성을 유지하였다.

---

### 거래 수정

```bash
python -m budget_app update \
  --id abc123 \
  --amount 30000 \
  --category food
```

- 거래 ID를 기준으로 기존 거래 내역을 수정하는 기능.

옵션으로 전달한 항목만 수정하며, 지정하지 않은 항목은 기존 값을 그대로 유지한다.

---

### 거래 삭제

```bash
python -m budget_app delete --id abc123
```

- 거래 ID를 기준으로 거래 내역을 삭제하는 기능.

존재하지 않는 거래 ID를 입력한 경우에는 오류 메시지를 출력하며, 삭제 후에는 `transactions.jsonl` 파일에 즉시 반영된다.

---

### CSV 내보내기

```bash
python -m budget_app export \
  --out output.csv \
  --month 2026-06
```

* 거래 내역을 CSV 파일로 저장하는 기능.

월 또는 기간 조건에 해당하는 거래 내역만 내보낼 수 있으며, 생성된 CSV 파일은 백업하거나 다른 프로그램에서 활용할 수 있다.

---

### CSV 가져오기

```bash
python -m budget_app import \
  --from transactions.csv
```

* CSV 파일에 저장된 거래 내역을 한 번에 가져오는 기능.

CSV 형식을 검증한 후 정상적인 데이터만 등록하며, 처리 결과와 등록 건수를 함께 출력한다.

---

## 4. 저장 파일

### transactions.jsonl

- 거래 내역 저장 파일

데이터의 추가와 수정이 빈번할 가계부 프로그램 속 **거래 내역**의 특징을 고려하여,
데이터를 한 줄씩 처리하는 jsonl 포맷을 채택하였다.

```json
{
  "id": "a1b2c3d4",
  "date": "2026-06-21",
  "type": "expense",
  "category": "food",
  "amount": 12000,
  "memo": "점심 식사",
  "tags": ["meal", "lunch"]
}
```

**jsonl의 장점**

- 스트리밍 처리 : 한 줄씩 읽고 처리하여 메모리 사용 효율이 좋다.
- 추가 및 수정 용이 : 데이터가 새로 추가될 때 파일 전체를 재작성하지 않고 한 줄씩 추가 가능하다.
- 에러 처리 : 특정 줄에 에러가 발생하더라도 해달 줄만 건너뛰거나 수정하여, 전체 파일에 영향을 주지 않는다. 

---

### categories.jsonl

- 사용 가능한 카테고리 목록 저장

거래 추가 및 수정 시 입력 가능한 카테고리를 관리하는 파일. 등록되지 않은 카테고리는 사용할 수 없으며, 사용자는 `category add`를 통해 새로운 카테고리를 등록할 수 있다. 

```json
[
  "food",
  "transport",
  "shopping",
  "salary"
]
```

---

### budgets.jsonl

- 월별 예산 저장

월별 예산을 Key - Value 형태로 관리한다. 

```json
{
  "2026-06": 500000,
  "2026-07": 600000
}
```


---


## 5. CSV 스키마

가져오기(import)와 내보내기(export)는 아래 형식을 사용.

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
2026-06-22,expense,food,12000,점심,"lunch,meal"
2026-06-25,income,salary,3000000,월급,payday
```

---

## 6. 구현 특징

### 제너레이터 기반 스트리밍

거래 내역 조회 및 검색 시 JSONL 파일 전체를 메모리에 올리지 않고 한 줄씩 읽어 처리.

```python
def stream_jsonl(self):
    with open(self.transactions_file, encoding="utf-8") as file:
        for line in file:
            yield json.loads(line)
```

---

### 데코레이터 활용

공통 기능(예외 처리, 실행 로그)를 데코레이터로 분리하였다.


---

### 타입 힌트 적용

함수의 입력값과 반환값을 명확하게 표현하여 가독성과 유지보수성을 향상시켰다.

```python
def get_transaction(self, transaction_id: str) -> Transaction | None:
    ...
```

---
### 종료 코드 부여

- 정상 종료 : exit code 0
- 오류 종류 : 0을 제외한 다른 exit code가 사용된다. 


### Q. 병목 관련

병목
- search : 전체 파일 순회
- summary : 전체 파일 순회
- update/delete : 전체 파일 재작성

개선방안
- category index
- month index
- chunk processing
- multiprocessing