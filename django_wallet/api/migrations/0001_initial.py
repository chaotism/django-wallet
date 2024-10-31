import django.core.validators
import django.db.models.deletion

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txid', models.CharField(max_length=255, unique=True)),
                ('amount', models.DecimalField(decimal_places=18, max_digits=32)),
            ],
            options={
                'db_table': 'transactions',
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                (
                    'balance',
                    models.DecimalField(
                        decimal_places=18,
                        max_digits=32,
                        validators=[django.core.validators.MinValueValidator(0)]
                    )
                ),
            ],
            options={
                'db_table': 'wallets',
            },
        ),
        migrations.AddConstraint(
            model_name='wallet',
            constraint=models.CheckConstraint(check=models.Q(('balance__gte', 0)), name='check_positive_balance'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.wallet'),
        ),
    ]
