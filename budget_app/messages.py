MESSAGES = {
    "ko": {
        "MENU_add": "- # 거래 추가 ---------------",
        "MENU_list": "- # 거래 목록 ---------------",
        "MENU_search": "- # 거래 검색 ---------------",
        "MENU_summary": "- # 월별 요약 ---------------",
        "MENU_delete": "- # 거래 삭제 ---------------",
        "MENU_update": "- # 거래 수정 ---------------",
        "MENU_category": "- # 카테고리 목록 --------------",

        "no_result": "검색 결과가 없습니다.",
        "complete_delete": "삭제가 완료되었습니다.",
        "complete_update": "수정이 완료되었습니다.",
        "complete_add": "추가가 완료되었습니다.",

        "ID_to_update": "수정할 거래 ID를 입력하세요.",
        "ID_to_delete": "삭제할 거래 ID를 입력하세요.",

        "CATE_to_add": "추가할 카테고리를 입력하세요.",
        "CATE_to_delete": "삭제할 카테고리를 입력하세요.",

        "cannot_delete_cate": "카테고리를 사용하는 거래가 있어 삭제할 수 없습니다.",
        "existing_cate": "이미 존재하는 카테고리입니다.",
        "exceed_budget": "예산을 초과하였습니다.",
        "no_data": "데이터가 존재하지 않습니다.",

        "ERR_not_found_id": "해당 ID의 거래가 존재하지 않습니다.",
        "ERR_not_valid_date": "날짜 형식이 올바르지 않습니다.",
        "ERR_not_valid_type": "거래 타입이 올바르지 않습니다. (income/expense)",
        "ERR_not_valid_amount": "양의 정수를 입력하세요.",
        "ERR_not_valid_cate": "존재하지 않는 카테고리입니다. 카테고리 등록 후 추가해주세요.",
        "ERR_export_command": "--month 또는 --from-date/--to-date 조건이 필요합니다.",

        "ERR_filenotfound": "[ERROR] 파일을 찾을 수 없습니다.",
        "ERR_value": "[ERROR] 잘못된 입력입니다.",
        "ERR_keyboardinter": "[ERROR] 사용자가 프로그램을 종료했습니다.",
        "ERR_except": "[ERROR] 예기치 않은 오류가 발생했습니다.",

        "HINT_filenotfound": "힌트 : 파일 경로와 파일명을 확인하세요.",
        "HINT_value": "힌트 : 입력 형식을 확인하세요.",
        "HINT_keyboardinter": "힌트 : 필요하면 프로그램을 다시 실행하세요.",
        "HINT_excpet": "힌트 : 입력값을 확인하거나 다시 시도하세요."
    }
}

def load_messages(lang: str = "ko") -> dict:
    return MESSAGES.get(lang, MESSAGES["ko"])