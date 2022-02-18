from tkinter import CASCADE
from django.db import models
from annoying.fields import AutoOneToOneField
from django.contrib.auth import get_user_model

User = get_user_model()
TRANSACTION_STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("SUCCESS", "SUCCESS"),
    ("UNDERWAY", "UNDERWAY"),
    ("FAILURE", "FAILURE"),
)

TRANSACTION_TYPE_CHOICES = (
    ("DEBIT", "DEBIT"),
    ("CREDIT", "CREDIT"),
)

class Wallet(models.Model):
    user = AutoOneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    points = models.PositiveSmallIntegerField(default=0)

    def operate(self, amount, hash=None, transac_stat=TRANSACTION_STATUS_CHOICES[1][0]):
        data = {}
        if(amount < 0 and abs(amount) > self.points):
            data['code'] = -1
            data['message'] = "You don't have enough points for that."
            return data

        r = WalletLedger.create_pending_record(self, amount)

        self.points = self.points + amount
        self.save()
    
        WalletLedger.success_pending_record(r)

        data['code'] = 1
        data['message'] = "Success!"
        data['balance'] = self.points
        return data

    def get_all_my_ledger(self):
        data = {}

        ledger = list(WalletLedger.objects.filter(wallet=self))
        if(len(ledger) <= 0):
            data['code'] = -1
            data['message'] = "no ledger record for your wallet"
            return data

        data['code'] = 1
        data['data'] = [d.as_dict() for d in ledger]
        return data

    def __str__(self):
        return 'wallet of user {}'.format(self.user.username)
    
class WalletLedger(models.Model):
    wallet = models.ForeignKey(
        Wallet, on_delete=models.CASCADE)


    change = models.IntegerField()
    initialWalletAmt = models.PositiveSmallIntegerField()
    finalWalletAmt = models.PositiveSmallIntegerField()

    trasaction_status = models.CharField(max_length=255, choices=TRANSACTION_STATUS_CHOICES)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPE_CHOICES)

    # Link to other models in simulators backend
    time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_pending_record(wallet, amt):
        if(amt < 0):
            transac_type = TRANSACTION_TYPE_CHOICES[0][0]
        else:
            transac_type = TRANSACTION_TYPE_CHOICES[1][0]

        ledger = WalletLedger.objects.create(wallet=wallet, change=amt, initialWalletAmt=wallet.points, finalWalletAmt=wallet.points+amt, trasaction_status=TRANSACTION_STATUS_CHOICES[0][0], transaction_type=transac_type)
        ledger.save()
        return ledger

    @staticmethod
    def success_pending_record(walletLedger):
        walletLedger.trasaction_status = TRANSACTION_STATUS_CHOICES[1][0]
        walletLedger.save()


    def __str__(self):
        return 'wallet ledger record: {}, amt {}, time {}'.format(self.wallet, self.amount, self.time)

    def as_dict(self):
        return {
            "user_id": self.wallet.user.id,
            "change": self.change,
            "initialAmt": self.initialWalletAmt,
            "finalAmt": self.finalWalletAmt,
            #"status": self.trasaction_status,
            "type": self.transaction_type,
            "time": self.time,
        }