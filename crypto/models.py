from django.db import models
from django.contrib.auth import get_user_model
from annoying.fields import AutoOneToOneField
from enum import Enum

User = get_user_model()

class CryptoBalance(models.Model):
    code = models.CharField(max_length=5)
    amount = models.FloatField()

class CryptoWallet(models.Model):
    user = AutoOneToOneField(User, related_name='crypto', on_delete=models.CASCADE)
    balance = models.ForeignKey(CryptoBalance, null=True, on_delete=models.CASCADE)

    def operate(self, crypto_id, amount):
        pass

    def get_all_ledger(self):
        data = {}

        ledger = list(CryptoWalletLedger.objects.filter(Cryptowallet=self))
        if(len(ledger) <= 0):
            data['code'] = -1
            data['message'] = "no ledger record for your crypto"
            return data

        data['code'] = 1
        data['data'] = []
        for d in ledger:
            data['data'].append(d.as_dict())
        return data



class ActionType(Enum):
    BUY="buy"
    SELL="sell"

class CryptoWalletLedger(models.Model):
    cryptowallet = models.ForeignKey(CryptoWallet, related_name='ledger', on_delete=models.CASCADE)
    action_type = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in ActionType])
    targetCrypto = models.CharField(max_length=5,)
    pricePerCrypto = models.FloatField()
    quantity = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)

    def as_dict(self):
        return {
            "id": self.id,
            "action": self.action_type,
            "targetCrypto": self.targetCrypto,
            "price": self.pricePerCrypto,
            "quantity": self.quantity,
            "created": self.created,
        }