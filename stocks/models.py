from django.db import models
from django.contrib.auth import get_user_model
from annoying.fields import AutoOneToOneField
from enum import Enum

User = get_user_model()

class StocksBalance(models.Model):
    code = models.CharField(max_length=5)
    amount = models.FloatField()

class StocksWallet(models.Model):
    user = AutoOneToOneField(User, related_name='stocks', on_delete=models.CASCADE)
    balance = models.ForeignKey(StocksBalance, null=True, on_delete=models.CASCADE)

    def operate(self, stock_id, amount):
        pass

    def get_all_ledger(self):
        data = {}

        ledger = list(StocksWalletLedger.objects.filter(stockwallet=self))
        if(len(ledger) <= 0):
            data['code'] = -1
            data['message'] = "no ledger record for your stocks"
            return data

        data['code'] = 1
        data['data'] = []
        for d in ledger:
            data['data'].append(d.as_dict())
        return data



class ActionType(Enum):
    BUY="buy"
    SELL="sell"

class StocksWalletLedger(models.Model):
    stockwallet = models.ForeignKey(StocksWallet, related_name='ledger', on_delete=models.CASCADE)
    action_type = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in ActionType])
    targetStock = models.CharField(max_length=5,)
    pricePerStock = models.FloatField()
    quantity = models.PositiveIntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {
            "id": self.id,
            "action": self.action_type,
            "targetStock": self.targetStock,
            "price": self.pricePerStock,
            "quantity": self.quantity,
            "created": self.created,
        }