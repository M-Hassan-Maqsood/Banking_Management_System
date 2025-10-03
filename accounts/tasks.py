from django.core.mail import send_mail
from decimal import Decimal

from BMS.celery import app
from BMS.choices import AccountType
from BMS.settings import DEFAULT_FROM_EMAIL


@app.task
def send_registration_email(user_email, account_id):
    subject = "New Account Created"
    message = f"Your new account (ID: {account_id}) has been created successfully."
    send_mail(
        subject,
        message,
        DEFAULT_FROM_EMAIL,
        [user_email],
    )

    print(f"[Celery] Email sent to {user_email} for account {account_id}")


@app.task
def calculate_daily_interest():
    accounts = AccountType.SAVING.value.objects.all()

    for account in accounts:
        interest = account.balance * Decimal("0.1")
        account.balance = account.balance + interest
        account.save()
