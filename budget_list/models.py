from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class BudgetList(models.Model):
    participants = models.ManyToManyField(User, related_name="+", blank=True)


class Budget(models.Model):
    budget_list = models.ForeignKey(
        BudgetList, on_delete=models.CASCADE, related_name="budgets"
    )
    name = models.CharField(max_length=50)


class Income(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="incomes")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=6)


class Expense(models.Model):
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name="expenses"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    amount = models.DecimalField(decimal_places=2, max_digits=6)
