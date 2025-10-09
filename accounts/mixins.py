from rest_framework.authtoken.models import Token

from accounts.factories import UserFactory


class AuthMixin:
    def setUpAuth(self):
        self.staff_user = UserFactory(is_staff=True)
        self.normal_user = UserFactory()
        self.other_user = UserFactory()

        self.staff_token = Token.objects.create(user=self.staff_user)
        self.normal_token = Token.objects.create(user=self.normal_user)
        self.other_token = Token.objects.create(user=self.other_user)

    def auth_as_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.staff_token.key)

    def auth_as_normal_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.normal_token.key)

    def auth_as_other_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.other_token.key)
