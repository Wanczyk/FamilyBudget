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

    def update(self, instance, validated_data):
        category_name = validated_data.pop("category")
        category = self._get_category_object(category_name)

        instance.category = category
        instance.name = validated_data.get('name', instance.name)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.save()
        return instance

    def to_representation(self, obj):
        self.fields['category'] = serializers.StringRelatedField(read_only=True)
        return super().to_representation(obj)


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


class BudgetListAddParticipantSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)

    class Meta:
        fields = ["username"]
