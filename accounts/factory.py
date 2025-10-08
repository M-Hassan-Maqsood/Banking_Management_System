from datetime import timezone

import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model

from banks.models import Bank, Branch
from accounts.models import Account


User = get_user_model()

class UserFactory(DjangoModelFactory):
    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    phone = factory.Faker("phone_number")
    date_of_birth = factory.Faker("date_of_birth", minimum_age=18)

    password = factory.PostGenerationMethodCall("set_password", "pass123")
    created_at = factory.Faker("past_datetime", start_date="-15d", tzinfo=timezone.utc)
    date_joined = factory.Faker("past_datetime", start_date="-15d", tzinfo=timezone.utc)

    class Meta:
        model = User


class BankFactory(DjangoModelFactory):
    name = factory.Faker("company")
    swift_code = factory.Faker("swift")
    established_date = factory.Faker("past_datetime")

    is_islamic = factory.Faker("boolean")
    created_at = factory.Faker("past_datetime", start_date="-15d", tzinfo=timezone.utc)

    class Meta:
        model = Bank


class BranchFactory(DjangoModelFactory):
    name = factory.Faker("city")
    bank = factory.SubFactory(BankFactory)
    branch_code = factory.Sequence(lambda n: f"B{n:03}")

    address = factory.Faker("address")
    created_at = factory.Faker("past_datetime", start_date="-15d", tzinfo=timezone.utc)

    class Meta:
        model = Branch


class AccountFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    branch = factory.SubFactory(BranchFactory)
    account_type = factory.Iterator(["CURRENT", "SAVINGS"])
    balance = factory.Faker("random_int", min=500, max=10000)

    is_active = factory.Faker("boolean")
    account_number = factory.Sequence(lambda n: 10000+n)
    created_at = factory.Faker("past_datetime", start_date="-15d", tzinfo=timezone.utc)

    class Meta:
        model = Account
