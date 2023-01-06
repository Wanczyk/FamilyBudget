from rest_framework import viewsets

from budget_list.models import BudgetList, Budget, Income, Expense
from budget_list.serializers import BudgetListSerializer, BudgetSerializer, IncomeSerializer, ExpenseSerializer


class BudgetListViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetListSerializer
    queryset = BudgetList.objects.all()

    def perform_create(self, serializer):
        participants = serializer.validated_data["participants"]
        if self.request.user not in participants:
            participants.append(self.request.user)
        serializer.save(participants=participants)


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()


class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
