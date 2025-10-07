from datetime import date

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token

from accounts.models import Account
from banks.models import Bank, Branch


class AccountAPIPermissionTests(APITestCase):
    def setUp(self):
        User = get_user_model()
        self.client = APIClient()

        common_fields = {
            "email": "example@gmail.com",
            "phone": "+923001112233",
            "date_of_birth": date(1999, 11, 5),
            "is_active": True,
        }

        self.staff_user = User.objects.create_user(username="admin", password="admin123", is_staff=True,
                                                   **common_fields)
        self.normal_user = User.objects.create_user(username="hassan", password="hassan123", is_staff=False,
                                                    **common_fields)
        self.other_user = User.objects.create_user(username="ali", password="ali123", is_staff=False, **common_fields)

        self.staff_token = Token.objects.create(user=self.staff_user)
        self.normal_token = Token.objects.create(user=self.normal_user)
        self.other_token = Token.objects.create(user=self.other_user)

        self.bank = Bank.objects.create(name="Test Bank", swift_code="TB001", established_date=date(2000, 1, 1))
        self.branch = Branch.objects.create(name="Main Branch", bank=self.bank)

        self.account1 = Account.objects.create(user=self.normal_user, branch=self.branch, account_type="Current",
                                               balance=500, account_number="1234567890")
        self.account2 = Account.objects.create(user=self.other_user, branch=self.branch, account_type="Savings",
                                               balance=1000, account_number="9876543210")
        self.url = reverse("account-list-create-api")

    def test_authentication_required_for_protected_endpoints(self):
        self.client.credentials()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.data)

    def test_normal_user_can_only_see_their_own_account(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["user"], self.normal_user.id)

    def test_staff_user_can_see_all_accounts(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    def test_user_can_update_own_balance(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        url = reverse('account-balance-api', args=[self.account1.id])
        response = self.client.patch(url, {"balance": 1500}, format='json')

        self.assertEqual(response.status_code, 200)
        self.account1.refresh_from_db()
        self.assertEqual(self.account1.balance, 1500)

    def test_user_cannot_update_others_balance(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        url = reverse('account-balance-api', args=[self.account2.id])
        response = self.client.patch(url, {"balance": 2000}, format='json')
        self.assertEqual(response.status_code, 403)

    def test_staff_can_update_any_balance(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        url = reverse('account-balance-api', args=[self.account2.id])
        response = self.client.patch(url, {"balance": 3000}, format='json')

        self.assertEqual(response.status_code, 200)
        self.account2.refresh_from_db()
        self.assertEqual(self.account2.balance, 3000)

    def test_filtering_and_search(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        response = self.client.get(self.url, {"account_type": "current"})
        self.assertEqual(response.status_code, 200)

        results = response.data.get("results", response.data)
        self.assertTrue(all(acc["account_type"] == "Current" for acc in results))
        response = self.client.get(self.url, {"search": "hassan"})
        self.assertEqual(response.status_code, 200)

        results = response.data.get("results", response.data)
        self.assertTrue(len(results) >= 1)
