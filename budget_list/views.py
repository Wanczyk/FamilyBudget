from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from budget_list.permissions import IsParticipant, HasBudgetlistPermission
from budget_list.models import BudgetList, Budget, Income, Expense
from budget_list.serializers import (
    BudgetListSerializer,
    BudgetSerializer,
    IncomeSerializer,
    ExpenseSerializer,
    BudgetListAddParticipantSerializer,
)
from budget_list.utils import create_income_expense


class BudgetListViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsParticipant]
    serializer_class = BudgetListSerializer

    def get_queryset(self, *args, **kwargs):
        return (
            BudgetList.objects.all()
            .order_by("id")
            .filter(participants__in=[self.request.user])
        )

    def perform_create(self, serializer):
        participants = serializer.validated_data["participants"]
        if self.request.user not in participants:
            participants.append(self.request.user)
        serializer.save(participants=participants)


class BudgetViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, HasBudgetlistPermission]
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data["budget_list"] = int(kwargs["budgetlist_pk"])
        serializer = BudgetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self, *args, **kwargs):
        return (
            Budget.objects.all()
            .order_by("id")
            .filter(budget_list__participants__in=[self.request.user])
        )


class IncomeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, HasBudgetlistPermission]
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()

    def list(self, request, budgetlist_pk=None, budget_pk=None):
        queryset = Income.objects.filter(
            budget__budget_list=budgetlist_pk, budget=budget_pk
        )
        serializer = IncomeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, budgetlist_pk=None, budget_pk=None):
        queryset = Income.objects.filter(
            pk=pk, budget=budget_pk, budget__budget_list=budgetlist_pk
        )
        income = get_object_or_404(queryset, pk=pk)
        serializer = IncomeSerializer(income)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serialized_data = create_income_expense(
            int(kwargs["budget_pk"]), request.data, IncomeSerializer
        )

        return Response(data=serialized_data, status=status.HTTP_201_CREATED)

    def get_queryset(self, *args, **kwargs):
        return (
            Income.objects.all()
            .order_by("id")
            .filter(budget__budget_list__participants__in=[self.request.user])
        )


class ExpenseViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated, HasBudgetlistPermission]
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

    def list(self, request, budgetlist_pk=None, budget_pk=None):
        queryset = Expense.objects.filter(
            budget__budget_list=budgetlist_pk, budget=budget_pk
        )
        serializer = ExpenseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, budgetlist_pk=None, budget_pk=None):
        queryset = Expense.objects.filter(
            pk=pk, budget=budget_pk, budget__budget_list=budgetlist_pk
        )
        expense = get_object_or_404(queryset, pk=pk)
        serializer = ExpenseSerializer(expense)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serialized_data = create_income_expense(
            int(kwargs["budget_pk"]), request.data, ExpenseSerializer
        )

        return Response(data=serialized_data, status=status.HTTP_201_CREATED)


class BudgetListAddParticipantViewSet(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, HasBudgetlistPermission]
    serializer_class = BudgetListAddParticipantSerializer

    def create(self, request, *args, **kwargs):
        serializer = BudgetListAddParticipantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(username=serializer.validated_data["username"])
        except User.DoesNotExist:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

        try:
            budget_list = BudgetList.objects.get(id=self.kwargs["pk"])
        except BudgetList.DoesNotExist:
            return Response("Budget not found", status=status.HTTP_404_NOT_FOUND)

        if user in budget_list.participants.all():
            return Response(
                "User already a participant", status=status.HTTP_409_CONFLICT
            )

        budget_list.participants.add(user)
        budget_list.save()

        return Response("User added", status=status.HTTP_200_OK)
