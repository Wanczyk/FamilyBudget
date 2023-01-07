def create_income_expense(budget_pk, request_data, serializer_class):
    request_data["budget"] = budget_pk
    serializer = serializer_class(data=request_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    return serializer.data
