from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from accounts.factories import AccountFactory, BankFactory, BranchFactory
from accounts.mixins import AuthMixin


class AccountAPIPermissionTest(AuthMixin, APITestCase):
    def setup(self):
        self.client = APIClient()
        self.set_up_auth()

        self.bank = BankFactory()
        self.branch = BranchFactory(bank=self.bank)

        self.account_1 = AccountFactory(user=self.normal_user, branch=self.branch)
        self.account_2 = AccountFactory(user=self.other_user, branch=self.branch)

        self.account_list_url = reverse("account-list-create-api")

    def test_authentication_protected_endpoints(self):
        self.client.credentials()
        response = self.client.get(self.account_list_url)

        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.data)

    def test_user_access_own_account(self):
        self.auth_as_normal_user()
        response = self.client.get(self.account_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["user"], self.normal_user.id)

    def test_staff_access_all_account(self):
        self.auth_as_staff()
        response = self.client.get(self.account_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    def test_user_update_balance(self):
        self.auth_as_normal_user()
        url = reverse('account-balance-api', args=[self.account_1.id])
        response = self.client.patch(url, {"balance": 1500}, format='json')

        self.account_1.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.account_1.balance, 1500)

    def test_user_cannot_update_others_balance(self):
        self.auth_as_normal_user()
        url = reverse('account-balance-api', args=[self.account_2.id])
        response = self.client.patch(url, {"balance": 2000}, format='json')

        self.assertEqual(response.status_code, 403)

    def test_staff_update_any_balance(self):
        self.auth_as_staff()
        url = reverse('account-balance-api', args=[self.account_2.id])
        response = self.client.patch(url, {"balance": 3000}, format='json')

        self.account_2.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.account_2.balance, 3000)

    def test_invalid_balance_update(self):
        self.auth_as_staff()
        url = reverse('staff-detail-api', args=[self.account_1.id])
        response = self.client.patch(url, {"balance": -100}, format='json')

        self.assertEqual(response.status_code, 400)

    def test_filter_and_search(self):
        self.auth_as_staff()
        response = self.client.get(self.account_list_url, {"account_type": "current"})

        self.assertEqual(response.status_code, 200)
        results = response.data.get("results", response.data)
        self.assertTrue(all(acc["account_type"] == "Current" for acc in results))
        response = self.client.get(self.account_list_url, {"search": self.normal_user.username})

        self.assertEqual(response.status_code, 200)
        results = response.data.get("results", response.data)
        self.assertTrue(len(results) >= 1)
