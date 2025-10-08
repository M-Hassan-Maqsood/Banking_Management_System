from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIRequestFactory
from unittest.mock import patch

from accounts.factory import UserFactory, AccountFactory, BankFactory, BranchFactory
from accounts.apis.permissions import IsStaffUser


class AccountAPIPermissionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.staff_user = UserFactory(is_staff=True, username="admin")
        self.normal_user = UserFactory(username="hassan")
        self.other_user = UserFactory(username="ali")

        self.staff_token = Token.objects.create(user=self.staff_user)
        self.normal_token = Token.objects.create(user=self.normal_user)
        self.other_token = Token.objects.create(user=self.other_user)

        self.bank = BankFactory()
        self.branch = BranchFactory(bank=self.bank)

        self.account_1 = AccountFactory(user=self.normal_user, branch=self.branch)
        self.account_2 = AccountFactory(user=self.other_user, branch=self.branch)

        self.account_list_url = reverse("account-list-create-api")

    def test_authentication_required_for_protected_endpoints(self):
        self.client.credentials()
        response = self.client.get(self.account_list_url)

        self.assertEqual(response.status_code, 401)
        self.assertIn("detail", response.data)

    def test_normal_user_access_own_account(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        response = self.client.get(self.account_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["user"], self.normal_user.id)

    def test_staff_user_access_all_account(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        response = self.client.get(self.account_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)

    def test_user_update_own_balance(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        url = reverse('account-balance-api', args=[self.account_1.id])
        response = self.client.patch(url, {"balance": 1500}, format='json')

        self.account_1.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.account_1.balance, 1500)

    def test_user_cannot_update_others_balance(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        url = reverse('account-balance-api', args=[self.account_2.id])
        response = self.client.patch(url, {"balance": 2000}, format='json')

        self.assertEqual(response.status_code, 403)

    def test_staff_can_update_any_balance(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        url = reverse('account-balance-api', args=[self.account_2.id])
        response = self.client.patch(url, {"balance": 3000}, format='json')

        self.account_2.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.account_2.balance, 3000)

    def test_filter_and_search(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        response = self.client.get(self.account_list_url, {"account_type": "current"})

        self.assertEqual(response.status_code, 200)
        results = response.data.get("results", response.data)
        self.assertTrue(all(acc["account_type"] == "Current" for acc in results))
        response = self.client.get(self.account_list_url, {"search": "hassan"})

        self.assertEqual(response.status_code, 200)
        results = response.data.get("results", response.data)
        self.assertTrue(len(results) >= 1)

    def test_permission_denied_for_non_owner(self):
        perm = IsStaffUser()
        factory = APIRequestFactory()
        request = factory.get('/')
        request.user = self.other_user
        self.assertFalse(perm.has_permission(request, None))

    def test_update_account_invalid_balance(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)
        url = reverse('staff-detail-api', args=[self.account_1.id])
        response = self.client.patch(url, {"balance": -100}, format='json')

        self.assertEqual(response.status_code, 400)

    @patch('accounts.apis.views.send_registration_email.delay')
    def test_create_account_triggers_email(self, mock_task):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)
        data = {
            "user": self.normal_user.id,
            "branch": self.branch.id,
            "account_type": "current",  # must match serializer choice
            "balance": 500,
            "account_number": "9876543210"  # unique
        }
        response = self.client.post(self.account_list_url, data, format='json')

        self.assertEqual(response.status_code, 201)
        mock_task.assert_called_once()
