from django.contrib.auth.models import User
from rest_framework import serializers

from budget_list.models import BudgetList, Budget, Income, Expense, Category


class IncomeExpenseBaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = Expense
        fields = ["id", "category", "name", "amount", "budget"]

    def _get_category_object(self, category_name):
        try:
            category = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            category = Category.objects.create(name=category_name)
        return category


class ExpenseSerializer(IncomeExpenseBaseSerializer):
    def create(self, validated_data):
        category_name = validated_data.pop("category")
        category = super()._get_category_object(category_name)
        expense = Expense.objects.create(category=category, **validated_data)
        return expense


class IncomeSerializer(IncomeExpenseBaseSerializer):
    def create(self, validated_data):
        category_name = validated_data.pop("category")
        category = super()._get_category_object(category_name)
        income = Income.objects.create(category=category, **validated_data)
        return income


class BudgetSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    incomes = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    expenses = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    budget_list = serializers.PrimaryKeyRelatedField(queryset=BudgetList.objects.all())

    class Meta:
        model = Budget
        fields = ["id", "name", "budget_list", "incomes", "expenses"]


class BudgetListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    budgets = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), default=list())

    class Meta:
        model = BudgetList
        fields = ["id", "participants", "budgets"]
