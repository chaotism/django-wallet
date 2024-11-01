from api.models import Transaction
from api.models import Wallet
from django.conf import settings
from rest_framework import serializers


class WalletSerializer(serializers.ModelSerializer):
    transactions = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ["id", "label", "balance", "transactions"]

    @staticmethod
    def get_transactions(obj):
        """
        Limiting the number of shown transactions for wallet preview
        """
        transactions = Transaction.objects.filter(wallet=obj).all()[: settings.WALLET_TRANSACTIONS_SHOW_LIMIT]
        return TransactionSerializer(transactions, many=True).data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "txid", "wallet", "amount"]  # txid is working as idempotency key
