from rest_framework import serializers
from banks.models import Bank


class BankSerializer(serializers.ModelSerializer):
    branch_count = serializers.IntegerField(read_only = True)

    class Meta:
        model = Bank
        fields = "__all__"


class BankNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ["name"]
