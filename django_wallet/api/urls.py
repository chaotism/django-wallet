from api.views import TransactionDetailAPIView
from api.views import TransactionListCreateAPIView
from api.views import WalletDetailAPIView
from api.views import WalletListCreateAPIView
from django.urls import path

urlpatterns = [
    path("wallets", WalletListCreateAPIView.as_view(), name="wallets"),
    path("wallets/<int:pk>/", WalletDetailAPIView.as_view(), name="wallet-detail"),
    path("transactions", TransactionListCreateAPIView.as_view(), name="transactions"),
    path("transactions/<int:pk>/", TransactionDetailAPIView.as_view(), name="transaction-detail"),
]
