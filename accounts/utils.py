from django.db.models import Sum, Case, When, Value, DecimalField, F
from django.db.models.functions import Coalesce
from decimal import Decimal

from BMS.choices import AmountType


def get_bank_analytics(transactions):
    bank_transaction = transactions.values(
        bank_id=F("account__branch__bank__id"),
        bank_name=F("account__branch__bank__name"),
        bank_is_islamic=F("account__branch__bank__is_islamic")
    ).annotate(
        total_deposits=Coalesce(Sum(
            Case(
                When(type=AmountType.Deposit.value, then=F("amount")),
                default=Value(0),
                output_field=DecimalField()
            )
        ), Value(Decimal("0.00"))
        ),
        total_withdrawals=Coalesce(Sum(
            Case(
                When(type=AmountType.Withdrawal.value, then=F("amount")),
                default=Value(0),
                output_field=DecimalField()
            )
        ), Value(Decimal("0.00"))
        )
    ).annotate(
        net=F("total_deposits") - F("total_withdrawals")
    )

    return bank_transaction

def get_branch_analytics(transactions):
    branch_transaction = transactions.values(
        bank_id=F("account__branch__bank__id"),
        branch_id=F("account__branch__id"),
        bank_name=F("account__branch__bank__name"),
        bank_is_islamic=F("account__branch__bank__is_islamic"),
        branch_name=F("account__branch__name")
    ).annotate(
        total_deposits=Coalesce(Sum(
            Case(
                When(type=AmountType.Deposit.value, then=F("amount")),
                default=Value(0),
                output_field=DecimalField()
            )
        ), Value(Decimal("0.00"))
        ),
        total_withdrawals=Coalesce(Sum(
            Case(
                When(type=AmountType.Withdrawal.value, then=F("amount")),
                default=Value(0),
                output_field=DecimalField()
            )
        ), Value(Decimal("0.00"))
        )
    ).annotate(
        net=F("total_deposits") - F("total_withdrawals")
    )

    return branch_transaction
