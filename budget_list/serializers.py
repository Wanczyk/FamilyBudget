from django.contrib.auth.models import User
from rest_framework import serializers

from budget_list.models import BudgetList, Budget, Income, Expense


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = "__all__"


class IncomeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Income
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = "__all__"


class BudgetListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    budgets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), default=list())

    class Meta:
        model = BudgetList
        fields = ["id", "participants", "budgets"]
