# Generated by Django 3.1.8 on 2022-02-19 23:43

import annoying.fields
import crypto.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crypto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.AlterField(
            model_name='cryptowallet',
            name='user',
            field=annoying.fields.AutoOneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='crypto', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='CryptoWalletLedger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(choices=[(crypto.models.ActionType['BUY'], 'buy'), (crypto.models.ActionType['SELL'], 'sell')], max_length=5)),
                ('targetCrypto', models.CharField(max_length=5)),
                ('pricePerCrypto', models.FloatField()),
                ('quantity', models.FloatField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('cryptowallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ledger', to='crypto.cryptowallet')),
            ],
        ),
        migrations.AddField(
            model_name='cryptowallet',
            name='balance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='crypto.cryptobalance'),
        ),
    ]
