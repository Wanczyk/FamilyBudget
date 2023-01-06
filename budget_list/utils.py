from budget_list.serializers import ExpenseSerializer


def create_income_expense(budget_pk, request_data):
    request_data["budget"] = budget_pk
    serializer = ExpenseSerializer(data=request_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.data
