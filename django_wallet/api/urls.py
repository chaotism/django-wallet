from django.urls import path

from api.views import WalletListCreateAPIView, WalletDetailAPIView
from api.views import TransactionListCreateAPIView, TransactionDetailAPIView

urlpatterns = [
    path("wallets", WalletListCreateAPIView.as_view(), name="wallets"),
    path("wallets/<int:pk>/", WalletDetailAPIView.as_view(), name="wallet-detail"),
    path("transactions", TransactionListCreateAPIView.as_view(), name="transactions"),
    path("transactions/<int:pk>/", TransactionDetailAPIView.as_view(), name="transaction-detail"),
]
