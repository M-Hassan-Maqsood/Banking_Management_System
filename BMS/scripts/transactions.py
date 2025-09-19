import random
import datetime

from banks.models import Bank, Branch
from users.models import User
from accounts.models import Account, Transaction


def generate_transactions():
    print("Creating banks and branches...")
    # Create Banks
    for row in range(4):
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        bank = Bank.objects.create(
            name = f"Bank_{row + 1}",
            swift_code = f"BANKPAK{row + 1:03}",
            is_islamic = random.choice([True, False]),
            established_date = datetime.date(row + 1978, month, day),
        )

        # Create Branches for each Bank
        Branch.objects.create(
            name=f"{bank.name}_Branch_{row + 1}",
            branch_code = f"{bank.id}{row + 1:02}",
            address = f"Street {random.randint(1,20)}, City {random.randint(1,5)}",
            bank = bank,
        )

    print("Creating users...")
    # Create Users
    for row in range(10):
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        User.objects.create(
            email = f"user{row + 1:03}@gmail.com",
            username = f"user{row + 1:03}",
            phone = f"+92333322{row + 2}",
            password = f"pas@Yt{row + 7}#U",
            date_of_birth = datetime.date(row + 1990, month, day),
        )

    print("Creating accounts and transactions...")
    # Create Accounts
    users = User.objects.all()
    banks = list(Bank.objects.all())

    for user in users:
        selected_banks = random.sample(banks, 2)
        for bank in selected_banks:
            branch = random.choice(bank.branches.all())
            account = Account.objects.create(
                user = user,
                branch = branch,
                account_number = random.randint(10000000, 99999999),
                account_type = random.choice(["saving", "current"]),
                balance = random.randint(1000, 50000),
            )

            # Create Transactions for each Account
            for transactions in range(random.randint(30, 50)):
                year = random.choice([2024, 2025])
                month = random.randint(1, 12)
                day = random.randint(1, 28)
                random_date = datetime.date(year, month, day)

                Transaction.objects.create(
                    date = random_date,
                    amount = random.randint(500, 50000),
                    type = random.choice(["deposit", "withdrawal"]),
                    account = account,
                )
    print("All transactions done")
