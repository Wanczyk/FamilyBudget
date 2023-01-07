from rest_framework import permissions

from budget_list.models import Budget, BudgetList, Expense, Income


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True if request.user in obj.participants.all() else False


class HasBudgetlistPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            budget_list_pk = view.kwargs["budgetlist_pk"]
        except KeyError:
            budget_list_pk = view.kwargs["pk"]

        try:
            budget_list = BudgetList.objects.get(id=budget_list_pk)
        except BudgetList.DoesNotExist:
            return True

        return True if request.user in budget_list.participants.all() else False
