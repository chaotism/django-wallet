from django.urls import path

from .views import TransactionAPIView
from .views import WalletListAPIView

urlpatterns = [
    path("wallets", WalletListAPIView.as_view(), name="wallets"),
    path("transactions", TransactionAPIView.as_view(), name="transactions"),
]
