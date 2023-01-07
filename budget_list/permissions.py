from rest_framework import permissions

from budget_list.models import Budget, BudgetList, Expense, Income


class IsParticipant(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        match obj:
            case BudgetList():
                return True if request.user in obj.participants.all() else False
            case Budget():
                return True if request.user in obj.budget_list.participants.all() else False
            case Expense() | Income():
                return True if request.user in obj.budget.budget_list.participants.all() else False
