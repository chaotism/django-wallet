from django.urls import path

from django_wallet.api.views import TransactionAPIView
from django_wallet.api.views import WalletListAPIView

urlpatterns = [
    path("wallets", WalletListAPIView.as_view(), name="wallets"),
    path("transactions", TransactionAPIView.as_view(), name="transactions"),
]
