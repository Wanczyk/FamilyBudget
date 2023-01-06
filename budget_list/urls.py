from django.urls import path, include
from rest_framework.routers import DefaultRouter
from budget_list import views


router = DefaultRouter()
router.register("budgetlists", views.BudgetListViewSet, basename="budgetlist")
router.register("budgets", views.BudgetViewSet, basename="budget")
router.register("incomes", views.IncomeViewSet, basename="income")
router.register("expenses", views.ExpenseViewSet, basename="expense")

urlpatterns = [
    path("", include(router.urls)),
]
