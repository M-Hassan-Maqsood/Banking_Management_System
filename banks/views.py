from django.views import View
from django.utils.decorators import method_decorator
from django.db.models import Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from banks.models import Bank


@method_decorator(login_required, name = "dispatch")
class BankListView(View):
    def get(self, request):
        banks = Bank.objects.all().annotate(branch_count = Count("branches"))
        data = [
            {
                "name": bank.name,
                "is_islamic": bank.is_islamic,
                "branch_count": bank.branch_count
            }
            for bank in banks
        ]
        return JsonResponse({"banks": data})
