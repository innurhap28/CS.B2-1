# 예산 전담
from storage.repository import Repository

class BudgetService:
    def __init__(self):
        self.repository = Repository()

    def set_budget(self, month: str, amount: int) -> None:
        budgets = self.repository.load_budgets()
        budgets[month] = amount
        self.repository.save_budgets(budgets)

    def get_budget(self, month:str) -> int | None:
        budgets = self.repository.load_budgets()
        return budgets.get(month)
    
    def calculate_usage(self, month: str, expense: int) -> tuple:
        budget = self.get_budget(month)
        if budget is None:
            return None, None, False
        usage = round((expense/budget)*100, 1)
        return budget, usage, expense > budget