from django.db import models
from django.contrib.auth import get_user_model

from enum import Enum
from annoying.fields import AutoOneToOneField
from datetime import datetime, timezone

User = get_user_model()

class DepositType(Enum):
    TENURE = "ontenure"
    WITHDRAWN = "withdrawn"
    BROKEN = "broken"
    FAILURE = "failure"


class InvestmentType(Enum):
    FD = "Fixed Deposit"
    CD = "Classic Deposit"
    
    @staticmethod
    def get_invest_data(t):
        if(t == InvestmentType.FD.value):
            return (7, 2)
        elif(t == InvestmentType.CD.value):
            return (4.5, 0)

        
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

    def withdraw(self, withdraw_id):
        data = {}
        record = BankLedger.objects.get(id=withdraw_id)
        if(DepositType.TENURE.value not in record.investment_status):
            data['code'] = -1
            data['message'] = "not a valid record"
            return data

        record.investment_status = DepositType.WITHDRAWN.value
        record.save()
        
        r = self.user.wallet.operate(record.current_amount)

        data['code'] = 1
        data['data'] = r
        return data


    def get_all_my_ledger(self):
        data = {}

        ledger = list(BankLedger.objects.filter(bank=self))
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
        now = datetime.now(timezone.utc)     
        time_elasped = now - self.lastUpdated
        mins = time_elasped.total_seconds() / 60

        year = int(mins)
        for i in range(year):
            self.current_amount += self.current_amount * (self.startingInterest / 100)

        self.lastUpdated = now
        self.save()

    @staticmethod
    def create_ledger_record(bank, amount, investment_type):
        startingInterest = InvestmentType.get_invest_data(investment_type)[0]
        investment_status = DepositType.TENURE.value
        ledger = BankLedger.objects.create(bank=bank, principle_amount=amount, current_amount=amount, startingInterest=startingInterest, investment_type=investment_type, investment_status=investment_status)
        ledger.save()
        return ledger

    def as_dict(self):
        return {
            "id": self.id,
            "invesType": self.investment_type,
            "inveStat": self.investment_status,
            "principle": self.principle_amount,
            #"status": self.trasaction_status,
            "current": self.current_amount,
            "roi": self.startingInterest,
            "tenure": self.tenure,
            "lastUpdated": self.lastUpdated,
            "created": self.created,
        }
