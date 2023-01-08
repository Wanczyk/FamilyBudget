from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class BudgetListTests(APITestCase):
    def setUp(self):
        url = reverse("rest_register")
        register_data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
        }
        self.user = self.client.post(url, register_data, format="json", follow=True)
        self.token = self.user.data["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def _create_budget_list(self):
        url = reverse("budgetlist-list")
        return self.client.post(url, {}, format="json")

    def _create_budget(self, budgetlist_pk):
        url = reverse("budget-list", args=[budgetlist_pk])
        data = {"name": "budget-name"}
        return self.client.post(url, data, format="json")

    def _create_expense(self, budgetlist_pk, budget_pk):
        url = reverse(
            "expense-list",
            kwargs={"budgetlist_pk": budgetlist_pk, "budget_pk": budget_pk},
        )
        data = {"name": "expense-name", "amount": 1.00, "category": "test_category"}
        return self.client.post(url, data, format="json")

    def _create_income(self, budgetlist_pk, budget_pk):
        url = reverse(
            "income-list",
            kwargs={"budgetlist_pk": budgetlist_pk, "budget_pk": budget_pk},
        )
        data = {"name": "income-name", "amount": 1.00, "category": "test_category"}
        return self.client.post(url, data, format="json")

    def test_creating_budget_list(self):
        response = self._create_budget_list()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_budget(self):
        budget_list_response = self._create_budget_list()
        response = self._create_budget(budget_list_response.data["id"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_expense(self):
        budget_list_response = self._create_budget_list()
        budget_response = self._create_budget(budget_list_response.data["id"])
        response = self._create_expense(
            budget_list_response.data["id"], budget_response.data["id"]
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_income(self):
        budget_list_response = self._create_budget_list()
        budget_response = self._create_budget(budget_list_response.data["id"])
        response = self._create_income(
            budget_list_response.data["id"], budget_response.data["id"]
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_participant(self):
        new_user = User.objects.create_user(
            username="newuser", password="newuserpass123"
        )

        budget_list_response = self._create_budget_list()
        url = reverse("add_participant", args=[budget_list_response.data["id"]])
        response = self.client.post(url, {"username": new_user.username}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
