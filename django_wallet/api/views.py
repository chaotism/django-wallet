from api.models import Transaction
from api.models import Wallet
from api.serializers import TransactionSerializer
from api.serializers import WalletSerializer
from django.db import IntegrityError
from rest_framework import filters
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView
from rest_framework_json_api import django_filters

# region wallet


class WalletListCreateAPIView(ListCreateAPIView):
    queryset = Wallet.objects.prefetch_related("transactions").all()
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
        "balance": (
            "gte",
            "lte",
        ),
    }
    ordering_fields = ["id", "label", "balance"]
    ordering = ["id"]


class WalletDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


# endregion wallet


# region transaction


class TransactionListCreateAPIView(ListCreateAPIView):
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
        "amount": (
            "gte",
            "lte",
        ),
    }
    ordering_fields = [
        "id",
    ]
    ordering = [
        "id",
    ]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            serializer.save()
        except IntegrityError:
            raise ValidationError({"error": "Transaction would result in negative wallet balance. Check balance"})


class TransactionDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request})
        return context


# endregion transaction
