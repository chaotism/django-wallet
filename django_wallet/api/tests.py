import decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Wallet, Transaction


class WalletAPITests(APITestCase):
    def setUp(self) -> None:
        self.wallet_1 = Wallet.objects.create(label="First Wallet", balance=100.0)
        self.wallet_2 = Wallet.objects.create(label="Second Wallet", balance=230.0)
        self.transaction_1_w1 = Transaction.objects.create(
            txid="init-txid-12345678",
            amount=70.0,
            wallet=self.wallet_1
        )
        self.transaction_2_w1 = Transaction.objects.create(
            txid="init-txid-87654321",
            amount=30.0,
            wallet=self.wallet_1
        )
        self.transaction_1_w2 = Transaction.objects.create(
            txid="init-txid-75849306",
            amount=230.0,
            wallet=self.wallet_2
        )

    def test_list_wallets(self) -> None:
        url = reverse("wallets")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallets = response.data["results"]
        self.assertEqual(len(wallets), 2)
        self.assertEqual(wallets[0]["label"], "First Wallet")
        self.assertEqual(wallets[1]["label"], "Second Wallet")

    def test_list_wallets_by_balance(self) -> None:
        url = reverse("wallets") + "?balance_from=200"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallets = response.data["results"]
        self.assertEqual(len(wallets), 1)
        self.assertEqual(wallets[0]["label"], "Second Wallet")

    def test_list_wallets_by_label(self) -> None:
        url = reverse("wallets") + "?label=first"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallets = response.data["results"]
        self.assertEqual(len(wallets), 1)
        self.assertEqual(wallets[0]["label"], "First Wallet")

    def test_list_wallets_order_by_desc(self) -> None:
        url = reverse("wallets") + "?order_by=balance"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallets = response.data["results"]
        self.assertEqual(len(wallets), 2)
        self.assertEqual(wallets[0]["label"], "First Wallet")
        self.assertEqual(wallets[1]["label"], "Second Wallet")

    def test_list_wallets_order_by_asc(self) -> None:
        url = reverse("wallets") + "?order_by=-balance"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        wallets = response.data["results"]
        self.assertEqual(len(wallets), 2)
        self.assertEqual(wallets[0]["label"], "Second Wallet")
        self.assertEqual(wallets[1]["label"], "First Wallet")

    def test_get_wallet(self) -> None:
        url = reverse("wallet-detail", kwargs={"pk": self.wallet_1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        received_wallet = response.data
        self.assertEqual(received_wallet["id"], self.wallet_1.id)
        self.assertEqual(received_wallet["label"], self.wallet_1.label)
        self.assertEqual(received_wallet["balance"], "100.000000000000000000")

    def test_create_wallet(self) -> None:
        url = reverse("wallets")
        new_wallet_payload = dict(label="Test Wallet", balance=1000)
        response = self.client.post(url, new_wallet_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_wallet = Wallet.objects.get(id=response.data["id"])
        self.assertEqual(new_wallet.balance, 0)
        self.assertEqual(new_wallet.label, "Test Wallet")

    def test_update_wallet(self) -> None:
        url = reverse("wallet-detail", kwargs={"pk": self.wallet_1.id})
        wallet_payload = {"label": "New Label"}
        response = self.client.patch(url, wallet_payload)
        new_wallet = Wallet.objects.get(id=response.data["id"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(new_wallet.label, "New Label")

    def test_delete_wallet(self) -> None:
        url = reverse("wallet-detail", kwargs={"pk": self.wallet_2.id})
        response = self.client.delete(url)
        try:
            wallet = Wallet.objects.get(id=self.wallet_2.id)
        except Wallet.DoesNotExist:
            wallet = None

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(wallet, None)
        deleted = response.data
        self.assertEqual(deleted["id"], self.wallet_2.id)
        self.assertEqual(deleted["label"], self.wallet_2.label)
        self.assertEqual(decimal.Decimal(deleted["balance"]), self.wallet_2.balance)

        # check existing of bind transactions to deleted wallet
        try:
            transaction = Transaction.objects.get(id=self.transaction_1_w2.id)
        except Transaction.DoesNotExist:
            transaction = None

        self.assertEqual(transaction, None)

        # check another wallet, which must exists
        wallet_1 = Wallet.objects.get(id=self.wallet_1.id)
        self.assertEqual(wallet_1.id, self.wallet_1.id)
        self.assertEqual(wallet_1.label, self.wallet_1.label)
        self.assertEqual(wallet_1.balance, self.wallet_1.balance)

    def tearDown(self):
        Transaction.objects.all().delete()
        Wallet.objects.all().delete()


class TransactionAPITests(APITestCase):
    def setUp(self):
        self.wallet_1 = Wallet.objects.create(label="First Wallet", balance=100.0)
        self.wallet_2 = Wallet.objects.create(label="Second Wallet", balance=230.0)
        self.transaction_1_w1 = Transaction.objects.create(
            txid="init-txid-12345678",
            amount=70.0,
            wallet=self.wallet_1
        )
        self.transaction_2_w1 = Transaction.objects.create(
            txid="init-txid-87654321",
            amount=30.0,
            wallet=self.wallet_1
        )
        self.transaction_1_w2 = Transaction.objects.create(
            txid="init-txid-75849306",
            amount=230.0,
            wallet=self.wallet_2
        )

    def test_list_transactions(self):
        url = reverse("wallet-transactions", kwargs={"wallet_pk": self.wallet_1.id})
        response = self.client.get(url)

        transactions = response.data["results"]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(transactions), 2)

    def test_list_transactions_by_amount(self) -> None:
        wallet_uri = reverse("wallet-transactions", kwargs={"wallet_pk": self.wallet_1.id})
        target_url = wallet_uri + "?amount_from=50"
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transactions = response.data["results"]
        self.assertEqual(len(transactions), 1)
        self.compare_transactions(transactions[0], self.transaction_1_w1)

    def test_list_transactions_by_txid(self) -> None:
        wallet_uri = reverse("wallet-transactions", kwargs={"wallet_pk": self.wallet_1.id})
        target_url = wallet_uri + f"?txid={self.transaction_1_w1.txid}"
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transactions = response.data["results"]
        self.assertEqual(len(transactions), 1)
        self.compare_transactions(transactions[0], self.transaction_1_w1)

    def test_list_transactions_order_by_desc(self) -> None:
        wallet_uri = reverse("wallet-transactions", kwargs={"wallet_pk": self.wallet_1.id})
        target_url = wallet_uri + "?order_by=amount"
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transactions = response.data["results"]
        self.assertEqual(len(transactions), 2)
        self.compare_transactions(transactions[0], self.transaction_2_w1)
        self.compare_transactions(transactions[1], self.transaction_1_w1)

    def test_list_transactions_order_by_asc(self) -> None:
        wallet_uri = reverse("wallet-transactions", kwargs={"wallet_pk": self.wallet_1.id})
        target_url = wallet_uri + "?order_by=-amount"
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transactions = response.data["results"]
        self.assertEqual(len(transactions), 2)
        self.compare_transactions(transactions[0], self.transaction_1_w1)
        self.compare_transactions(transactions[1], self.transaction_2_w1)

    def test_get_transaction(self) -> None:
        url = reverse(
            "wallet-transaction-detail",
            kwargs={
                "wallet_pk": self.transaction_1_w2.wallet.id,
                "pk": self.transaction_1_w2.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        received = response.data
        self.compare_transactions(received, self.transaction_1_w2)

    def test_create_transaction(self) -> None:
        url = reverse("wallet-transactions", kwargs={"wallet_pk": self.wallet_2.id})
        new_transaction_payload = dict(txid="test-txid-12345678", amount="0.00000000000009")
        response = self.client.post(url, new_transaction_payload)
        new_transaction = Transaction.objects.get(id=response.data["id"])
        wallet = Wallet.objects.get(id=response.data["wallet"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.compare_transactions(response.data, new_transaction)

        self.assertEqual(wallet.balance, decimal.Decimal("230.00000000000009"))

    def test_create_transaction_with_zero_amount(self) -> None:
        url = reverse("wallet-transactions", kwargs={"wallet_pk": self.wallet_2.id})
        new_transaction_payload = dict(txid="test-txid-12345672", amount="0")
        response = self.client.post(url, new_transaction_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transaction_with_negative_amount_more_than_wallet_balance(self) -> None:
        url = reverse("wallet-transactions", kwargs={"wallet_pk": self.wallet_2.id})
        new_transaction_payload = dict(txid="test-txid-22345672", amount="-235")
        response = self.client.post(url, new_transaction_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_transaction_with_duplicate_txid(self) -> None:
        url = reverse("wallet-transactions", kwargs={"wallet_pk": self.wallet_1.id})
        new_transaction_payload = dict(txid=self.transaction_1_w1.txid, amount="100")
        response = self.client.post(url, new_transaction_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_transaction(self) -> None:
        url = reverse(
            "wallet-transaction-detail",
            kwargs={
                "wallet_pk": self.transaction_1_w2.wallet.id,
                "pk": self.transaction_1_w2.id
            }
        )
        transaction_payload = dict(amount=decimal.Decimal("1000.000009"))
        response = self.client.patch(url, transaction_payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_replace_transaction(self) -> None:
        url = reverse(
            "wallet-transaction-detail",
            kwargs={
                "wallet_pk": self.transaction_1_w1.wallet.id,
                "pk": self.transaction_1_w1.id
            }
        )
        transaction_payload = dict(id=19, txid="random_txid_736453", amount=decimal.Decimal("1000.000009"))
        response = self.client.put(url, transaction_payload)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_transaction(self) -> None:
        url = reverse(
            "wallet-transaction-detail",
            kwargs={
                "wallet_pk": self.transaction_1_w1.wallet.id,
                "pk": self.transaction_1_w1.id
            }
        )
        response = self.client.delete(url)
        try:
            transaction = Transaction.objects.get(id=response.data["id"])
        except Transaction.DoesNotExist:
            transaction = None

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(transaction, None)
        deleted = response.data
        self.compare_transactions(deleted, self.transaction_1_w1)

        wallet_1 = Wallet.objects.get(id=self.transaction_1_w1.wallet.id)
        self.assertEqual(wallet_1.balance, self.wallet_1.balance - self.transaction_1_w1.amount)

    def compare_transactions(self, response: dict, model: Transaction) -> None:
        # tool function to compare transaction received from api response and example transaction
        self.assertEqual(response["id"], model.id)  # type: ignore
        self.assertEqual(response["wallet"], model.wallet.id)
        self.assertEqual(response["txid"], model.txid)
        self.assertEqual(decimal.Decimal(response["amount"]), model.amount)

    def tearDown(self):
        Transaction.objects.all().delete()
        Wallet.objects.all().delete()
