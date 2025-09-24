import datetime
from decimal import Decimal
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Case, When, Sum, Max, DecimalField, F, Value, Min
from django.db.models.functions import Coalesce
from django.db.models import Window
from rest_framework.response import Response
from rest_framework import status

from BMS.choices import AccountType, AmountType
from accounts.apis.permissions import IsStaffUser
from accounts.serializers import AccountSerializer, AccountSummarySerializer
from accounts.models import Account, Transaction


class AccountListCreateAPIView(ListCreateAPIView):
    serializer_class = AccountSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["branch__bank__name", "account_type", "branch__bank__is_islamic"]
    search_fields = ["user__first_name", "user__last_name", "user__username"]
    ordering_fields = ["balance", "created_at", "user__username"]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Account.objects.all()

        return Account.objects.filter(user = self.request.user)


class AccountBalanceUpdateAPIView(UpdateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_object(self):
        account = super().get_object()
        if self.request.user.is_staff or account.user == self.request.user:
            return account
        raise PermissionDenied("You are not allowed to access this account")


class StaffAccountDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsStaffUser]


class SummaryAPIView(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        account_id = kwargs.get("pk")

        account = Account.objects.get(id = account_id)
        if not account:
            return Response({"Account does not found"},status=status.HTTP_404_NOT_FOUND)

        if month and year:
            start_date = datetime.date(int(year), int(month), 1)
        elif year:
            start_date = datetime.date(int(year), 1, 1)
        else:
            start_date = None

        txn = Transaction.objects.filter(account_id = account_id)

        if year:
            txn = txn.filter(date__year = year)
        if month:
            txn = txn.filter(date__month = month)

        report = txn.aggregate(
            deposit_case = Coalesce(
                Sum(
                Case(
                    When(type = AmountType.Deposit.value, then = F("amount")),
                    default = Value(0),
                    output_field = DecimalField()
                )
                    ), Value(Decimal("0.00"))
            ),

            withdrawal_case=Coalesce(Sum(
                Case(
                    When(type = AmountType.Withdrawal.value, then = F("amount")),
                    default = Value(0),
                    output_field = DecimalField()
                )
            ), Value(Decimal("0.00"))
            ),
            max_txn_amount = Coalesce(Max("amount"),Value(Decimal("0.00")))
        )

        annotate = txn.annotate(
            running_balance= Coalesce(Window(
                expression = Sum(
            Case(
                When(type = AmountType.Deposit.value, then = F("amount")),
                When(type = AmountType.Withdrawal.value, then = F("amount")),
                default = Value(0),
                output_field = DecimalField(),
            )
        ),
            order_by = ["date","id"]
                ), Value(Decimal("0.00"))
            )
        )

        opening_balance = Transaction.objects.filter(
            account_id = account_id,
            date__lt = start_date,
        ).aggregate(
            balance = Coalesce(
                Sum(
                Case(
                When(type = AmountType.Deposit.value, then = F("amount")),
                When(type = AmountType.Withdrawal.value, then = -F("amount")),
                default = Value(0),
                output_field = DecimalField(),
                )
                ), Value(Decimal("0.00"))
            )
        )["balance"]

        lowest_balance = annotate.aggregate(
            min_balance = Coalesce(
            Min("running_balance"),
                Value(Decimal("0.00"))
            )
        )["min_balance"]

        data = {
            "account_id": account.id,
            "opening_balance": opening_balance,
            "total_deposits": report["deposit_case"],
            "total_withdrawals": report["withdrawal_case"],
            "max_txn_amount": report["max_txn_amount"],
            "min_running_balance": lowest_balance,
        }

        serializer = AccountSummarySerializer(data)
        return Response(serializer.data, status = status.HTTP_200_OK)
