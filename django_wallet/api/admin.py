from django.contrib import admin

from .models import Transaction
from .models import Wallet


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    raw_id_fields = ("wallet",)
    list_display = (
        "id",
        "wallet_id",
        "txid",
        "amount",
    )
    readonly_fields = ("txid", "amount",)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "label",
        "balance",
    )
    readonly_fields = ("balance",)
