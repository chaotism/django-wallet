from django.db import IntegrityError
from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView
from rest_framework_json_api import django_filters
from rest_framework_json_api import filters

from .models import Transaction
from .models import Wallet
from .serializers import TransactionSerializer
from .serializers import WalletSerializer


class WalletListAPIView(ListAPIView, CreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
    ]
    filterset_fields = {
        "id": ("exact",),
        "label": (
            "icontains",
            "iexact",
        ),
        "balance":(
            "gte",
            "lte",
        )
    }
    ordering_fields = ["id", "label", "balance"]
    ordering = ["id"]


class TransactionAPIView(ListAPIView, CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
    ]
    filterset_fields = {
        "id": ("exact",),
        "txid": ("exact",),
        "wallet_id": ("exact",),
        "balance": (
            "gte",
            "lte",
        )
    }
    ordering_fields = [
        "id",
    ]
    ordering = [
        "id",
    ]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            wallet = serializer.validated_data["wallet"]
            wallet.balance = F("balance") + serializer.validated_data["amount"]
            wallet.save()
        except IntegrityError:
            raise ValidationError({"error": "Transaction would result in negative wallet balance. Check balance"})

        serializer.save()
