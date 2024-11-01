from decimal import Decimal
from unittest.mock import ANY
from uuid import uuid4

import pytest
from django.test import Client
from django.urls import reverse

from api.models import Wallet, Transaction


# @pytest.fixture(scope=session, autouse=True)  # TODO: update django conf instead simple load env
# def load_env(name='.env.test'):
#     # Load virtual variables on local test run
#     load_dotenv(settings.BASE_DIR + name)


@pytest.fixture(scope="session")
def client():
    return Client()


@pytest.fixture(autouse=True)
def clear_data():
    yield
    Transaction.objects.all().delete()
    Wallet.objects.all().delete()


@pytest.fixture()
def wallet(label:str='label', balance: float=0.0):
    return Wallet.objects.create(label=label, balance=Decimal(balance))


@pytest.fixture()
def transaction(wallet, amount: float = 0):
    return Transaction.objects.create(txid=str(uuid4()), amount=Decimal(amount), wallet=wallet)


# TODO: split to submodules
# region wallet

@pytest.mark.django_db
def test_wallet_list(client, wallet, transaction):
    url = reverse("wallets")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            {
                'id': 1,
                'label': 'label',
                'balance': '0.000000000000000000',
                'transactions': [
                    {
                        'id': 1,
                        'txid': ANY,
                        'wallet': 1,
                        'amount': '0.000000000000000000'
                    }
                ]
            }
        ]
    }


@pytest.mark.parametrize(
    "balance, label, response_code",
    [
        (0, 'test', 201),
        (0, '', 400),
        (2*64, 'test', 201),
        (-1, 'test', 400)
    ]
)
@pytest.mark.django_db
def test_wallet_create(client, balance, label, response_code):
    url = reverse("wallets")
    response = client.post(url, data={'balance': balance, 'label': label})
    assert response.status_code == response_code


@pytest.mark.xfail(reason='not ready')
@pytest.mark.django_db
def test_wallet_update(client, balance, label, response_code):
    raise NotImplemented


@pytest.mark.xfail(reason='not ready')
@pytest.mark.django_db
def test_wallet_delete(client, balance, label, response_code):
    raise NotImplemented


@pytest.mark.xfail(reason='not ready')
@pytest.mark.django_db
def test_wallet_filters(client, wallet, transaction):
    raise NotImplemented

# endregion wallet


# region transaction

@pytest.mark.django_db
def test_transaction_list(client, wallet, transaction):
    url = reverse("transactions")
    response = client.get(url)
    assert response.status_code == 200
    assert response.json() == {
        'count': 1,
        'next': None,
        'previous': None,
        'results': [
            {
                'id': ANY,
                'txid': ANY,
                'wallet': ANY,
                'amount': '0.000000000000000000'
            }
        ]
    }


@pytest.mark.parametrize(
    "amount, response_code",
    [
        (0, 201),
        (2*64, 201),
        (-1, 400)
    ]
)
@pytest.mark.django_db
def test_transaction_create(client, wallet, amount, response_code):
    url = reverse("transactions")
    response = client.post(url, data={'txid':str(uuid4()), 'wallet': wallet.pk, 'amount': amount})
    assert response.status_code == response_code


@pytest.mark.xfail(reason='not ready')
@pytest.mark.django_db
def test_transaction_update(client, balance, label, response_code):
    raise NotImplemented


@pytest.mark.xfail(reason='not ready')
@pytest.mark.django_db
def test_transaction_delete(client, balance, label, response_code):
    raise NotImplemented


@pytest.mark.xfail(reason='not ready')
@pytest.mark.django_db
def test_transaction_filters(client, wallet, transaction):
    raise NotImplemented

# endregion transaction
