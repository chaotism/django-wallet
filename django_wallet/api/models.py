from django.core.validators import MinValueValidator
from django.db import models
from django.db import transaction
from django.db.models import CheckConstraint
from django.db.models import Q
from django.shortcuts import get_object_or_404


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField(max_digits=32, decimal_places=18, validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.pk}-{self.label}: {self.balance}"

    class Meta:
        db_table = "wallets"
        constraints = [
            CheckConstraint(
                check=Q(balance__gte=0),
                name="check_positive_balance",
            ),
        ]


class Transaction(models.Model):
    txid = models.CharField(max_length=255, unique=True)  # noqa
    wallet = models.ForeignKey(Wallet, related_name="transactions", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=32, decimal_places=18)

    def __str__(self):
        return f"{self.pk}-{self.txid}: {self.amount}"

    class Meta:
        db_table = "transactions"

    @transaction.atomic
    def save(self, *args, **kwargs):
        wallet = get_object_or_404(Wallet.objects.select_for_update(), pk=self.wallet.pk)
        wallet.balance += self.amount
        wallet.save()
        super(Transaction, self).save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        wallet = get_object_or_404(Wallet.objects.select_for_update(), pk=self.wallet.pk)
        wallet.balance -= self.amount
        wallet.save()
        super(Transaction, self).save(*args, **kwargs)
