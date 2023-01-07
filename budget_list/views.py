from django.contrib.auth.models import User
from rest_framework import viewsets, generics, status
from rest_framework.response import Response

from budget_list.permissions import IsParticipant
from budget_list.models import BudgetList, Budget, Income, Expense
from budget_list.serializers import BudgetListSerializer, BudgetSerializer, IncomeSerializer, ExpenseSerializer, \
    BudgetListAddParticipantSerializer
from budget_list.utils import create_income_expense


class BudgetListViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipant]
    serializer_class = BudgetListSerializer

    def get_queryset(self, *args, **kwargs):
        return BudgetList.objects.all().order_by('id').filter(participants__in=[self.request.user])

    def perform_create(self, serializer):
        participants = serializer.validated_data["participants"]
        if self.request.user not in participants:
            participants.append(self.request.user)
        serializer.save(participants=participants)


class BudgetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipant]
    serializer_class = BudgetSerializer
    queryset = Budget.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data["budget_list"] = int(kwargs["budgetlist_pk"])
        serializer = BudgetSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=serializer.data)


class IncomeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipant]
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()

    def create(self, request, *args, **kwargs):
        serialized_data = create_income_expense(int(kwargs["budget_pk"]), request.data, IncomeSerializer)

        return Response(data=serialized_data)


class ExpenseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsParticipant]
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

    def create(self, request, *args, **kwargs):
        serialized_data = create_income_expense(int(kwargs["budget_pk"]), request.data, ExpenseSerializer)

        return Response(data=serialized_data)


class BudgetListAddParticipantViewSet(generics.CreateAPIView):
    permission_classes = [IsParticipant]
    serializer_class = BudgetListAddParticipantSerializer

    def create(self, request, *args, **kwargs):
        serializer = BudgetListAddParticipantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.get(username=serializer.validated_data["username"])
        budget_list = BudgetList.objects.get(id=self.kwargs["pk"])

        if user in budget_list.participants.all():
            return Response("User already a participant", status=status.HTTP_409_CONFLICT)

        budget_list.participants.add(user)
        budget_list.save()

        return Response("User added", status=status.HTTP_200_OK)


