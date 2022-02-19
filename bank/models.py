from decimal import Decimal
from tracemalloc import start
from django.contrib.auth.models import AbstractUser
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
)
from django.db import models

from .managers import UserManager

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

MALE = 'M'
FEMALE = 'F'

GENDER_CHOICE = (
    (MALE, "Male"),
    (FEMALE, "Female"),
)

# class User(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True, null=False, blank=False)

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

#     def __str__(self):
#         return self.email

#     @property
#     def balance(self):
#         if hasattr(self, 'account'):
#             return self.account.balance
#         return 0


class BankAccountType(models.Model):
    name = models.CharField(max_length=128)
    maximum_withdrawal_amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    annual_interest_rate = models.DecimalField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        decimal_places=2,
        max_digits=5,
        help_text='Interest rate from 0 - 100'
    )
    interest_calculation_per_year = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        help_text='The number of times interest will be calculated per year'
    )

    def __str__(self):
        return self.name

    def calculate_interest(self, principal):
        """
        Calculate interest for each account type.

        This uses a basic interest calculation formula
        """
        p = principal
        r = self.annual_interest_rate
        n = Decimal(self.interest_calculation_per_year)

        # Basic Future Value formula to calculate interest
        interest = (p * (1 + ((r/100) / n))) - p

        return round(interest, 2)


class UserBankAccount(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    account_type = models.ForeignKey(
        BankAccountType,
        related_name='accounts',
        on_delete=models.CASCADE
    )
    account_no = models.PositiveIntegerField(unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    interest_start_date = models.DateField(
        null=True, blank=True,
        help_text=(
            'The month number that interest calculation will start from'
        )
    )
    initial_deposit_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.account_no)

    def get_interest_calculation_months(self):
        """
        List of month numbers for which the interest will be calculated

        returns [2, 4, 6, 8, 10, 12] for every 2 months interval
        """
        interval = int(
            12 / self.account_type.interest_calculation_per_year
        )
        start = self.interest_start_date.month
        return [i for i in range(start, 13, interval)]


class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.PositiveIntegerField()
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.email


from enum import Enum
from annoying.fields import AutoOneToOneField

class DepositType(Enum):
    TENURE = "ontenure"
    WITHDRAWN = "withdrawn"
    BROKEN = "broken"
    FAILURE = "failure"

    def __repr__(self):
        return self.value

class InvestmentType(Enum):
    FD = "Fixed Deposit"
    CD = "Classic Deposit"

    @staticmethod
    def get_invest_data(t):
        if(t == InvestmentType.FD.value):
            return (7, 2)
        elif(t == InvestmentType.CD.value):
            return (4.5, 0)

    def __repr__(self):
        return self.value

class Bank(models.Model):
    user = AutoOneToOneField(User, related_name='bank', on_delete=models.CASCADE)

    def operate(self, amount, invest_type=InvestmentType.CD, tenure=0):
        data = {}
        if(amount > self.user.wallet.points):
            data['code'] = -1
            data['message'] = "not enough points to invest"
            return data

        ledger = BankLedger.create_ledger_record(self, amount, invest_type)
        data['code'] = 1
        data['data'] = ledger.as_dict()
        return data

    def get_all_my_ledger(self):
        data = {}

        ledger = list(BankLedger.objects.filter(wallet=self))
        if(len(ledger) <= 0):
            data['code'] = -1
            data['message'] = "no ledger record for your bank"
            return data

        data['code'] = 1
        data['data'] = []
        for d in ledger:
            d.update_deposit_ledger()
            data['data'].append(d.as_dict())
        return data


class BankLedger(models.Model):
    bank = models.ForeignKey(Bank, related_name='ledger', on_delete=models.CASCADE)
    investment_type = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in InvestmentType])
    investment_status = models.CharField(max_length=255, choices=[(tag, tag.value) for tag in DepositType])

    principle_amount = models.PositiveIntegerField()
    current_amount = models.PositiveIntegerField()
    startingInterest = models.FloatField()
    tenure = models.PositiveIntegerField(default=0)

    lastUpdated = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)

    def update_deposit_ledger(self):
        pass

    @staticmethod
    def create_ledger_record(bank, amount, investment_type):
        startingInterest = InvestmentType.get_invest_data(investment_type)[0]
        investment_status = DepositType.TENURE
        ledger = BankLedger.objects.create(bank=bank, principle_amount=amount, current_amount=amount, startingInterest=startingInterest, investment_type=investment_type, investment_status=investment_status)
        ledger.save()
        return ledger

    def as_dict(self):
        return {
            "invesType": str(self.investment_type),
            "inveStat": str(self.investment_status),
            "principle": self.principle_amount,
            #"status": self.trasaction_status,
            "current": self.current_amount,
            "roi": self.startingInterest,
            "tenure": self.tenure,
            "lastUpdated": self.lastUpdated,
            "created": self.created,
        }
