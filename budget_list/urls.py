from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from budget_list import views

router = DefaultRouter()
router.register("budgetlists", views.BudgetListViewSet, basename="budgetlist")

budgetlist_router = routers.NestedSimpleRouter(
    router, r"budgetlists", lookup="budgetlist"
)
budgetlist_router.register("budgets", views.BudgetViewSet, basename="budget")

budget_router = routers.NestedSimpleRouter(
    budgetlist_router, r"budgets", lookup="budget"
)
budget_router.register(r"incomes", views.IncomeViewSet, basename="income")
budget_router.register(r"expenses", views.ExpenseViewSet, basename="expense")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(budgetlist_router.urls)),
    path(r"", include(budget_router.urls)),
    path(
        "budgetlists/<int:pk>/add-participant/",
        views.BudgetListAddParticipantViewSet.as_view(),
        name="add_participant",
    ),
]
