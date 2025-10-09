from rest_framework.authtoken.models import Token

from accounts.factories import UserFactory


class AuthMixin:
    def setup_auth(self):
        self.staff_user = UserFactory(is_staff=True)
        self.user = UserFactory()

        self.staff_token = Token.objects.create(user=self.staff_user)
        self.user_token = Token.objects.create(user=self.user)

    def auth_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)

    def auth_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)

