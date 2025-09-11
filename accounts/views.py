from django.views import View
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accounts.models import Account


@method_decorator(login_required, name = "dispatch")
class AccountListView(View):
    def get(self, request):
        accounts = Account.objects.all().select_related("branch__bank")
        data = [
            {
                "bank_name": account.branch.bank.name,
                "account_number": account.account_number,
                "balance": account.balance
            }
            for account in accounts
        ]

        return JsonResponse({"accounts": data})
