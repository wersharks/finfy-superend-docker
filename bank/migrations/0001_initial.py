# Generated by Django 4.0.2 on 2022-02-19 09:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BankAccountType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('maximum_withdrawal_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('annual_interest_rate', models.DecimalField(decimal_places=2, help_text='Interest rate from 0 - 100', max_digits=5, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('interest_calculation_per_year', models.PositiveSmallIntegerField(help_text='The number of times interest will be calculated per year', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
            ],
        ),
        migrations.CreateModel(
            name='UserBankAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.PositiveIntegerField(unique=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('interest_start_date', models.DateField(blank=True, help_text='The month number that interest calculation will start from', null=True)),
                ('initial_deposit_date', models.DateField(blank=True, null=True)),
                ('account_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='bank.bankaccounttype')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_address', models.CharField(max_length=512)),
                ('city', models.CharField(max_length=256)),
                ('postal_code', models.PositiveIntegerField()),
                ('country', models.CharField(max_length=256)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]