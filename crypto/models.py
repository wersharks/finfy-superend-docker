from django.db import models
from django.contrib.auth import get_user_model
from annoying.fields import AutoOneToOneField
from enum import Enum

from numpy import quantile, true_divide
from .const import COINS_MARKET
from pycoingecko import CoinGeckoAPI

User = get_user_model()

class CryptoWallet(models.Model):
    user = AutoOneToOneField(User, related_name='crypto', on_delete=models.CASCADE)

    def buy(self, crypto_id, amount):
        data = {}
        if(not CryptoWallet.isValidCryptId(crypto_id)):
            data['code'] = -1
            data['message'] = "not a valid crypto"
            return data
        
        cdata = CryptoWallet.get_coin_data(crypto_id)
        price = cdata[crypto_id]['inr']
        if(amount * price > self.user.wallet.points):
            data['code'] = -1
            data['message'] = "not enough money for this transaction"
            return data

        # get all wallets with crypto_id
        bal = CryptoBalance.objects.filter(cryptowallet=self, code=crypto_id)
        if(bal.exists()):
            # Already wallet there so add some
            rc = bal[0]
            rc.amount += amount
            rc.save()
        else:
            # Create new wallet
            new_rc = CryptoBalance(cryptowallet=self, code=crypto_id, amount=amount)
            new_rc.save()

        self.user.wallet.operate(amount * price * -1)

        x = CryptoWalletLedger.create_ledger_record(self, ActionType.BUY, crypto_id, price, amount)

        data['code'] = 1
        data['message'] = "Success"
        data['wallet'] = self.wallet_data()
        data['ledger'] = x
        return data

    def sell(self, crypto_id, amount):
        data = {}
        if(not CryptoWallet.isValidCryptId(crypto_id)):
            data['code'] = -1
            data['message'] = "not a valid crypto"
            return data
        
        cdata = CryptoWallet.get_coin_data(crypto_id)
        price = cdata[crypto_id]['inr']

        bal = CryptoBalance.objects.filter(cryptowallet=self, code=crypto_id)
        if(not bal.exists() or not bal[0].amount>amount):
            data['code'] = -1
            data['message'] = "you don't have enough crypto for this transaction."
        
        r = bal[0]
        r.amount -= amount
        r.save()

        points = price * amount
        self.user.wallet.operate(points)

        x = CryptoWalletLedger.create_ledger_record(self, ActionType.SELL, crypto_id, price, amount)

        data['code'] = 1
        data['message'] = "Success"
        data['wallet'] = self.wallet_data()
        data['ledger'] = x
        return data

    def wallet_data(self):
        data = list(CryptoBalance.objects.filter(cryptowallet=self))
        if(len(data)>0):
            return [d.as_dict() for d in data]
        else:
            return {}

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

    @staticmethod
    def isValidCryptId(id):
        if(id in COINS_MARKET):
            return True
        else: return False

    @staticmethod
    def get_coin_data(coin_id):
        cg = CoinGeckoAPI()
        d = cg.get_price(ids=coin_id, vs_currencies='inr')
        return d

class CryptoBalance(models.Model):
    cryptowallet = models.ForeignKey(CryptoWallet, related_name='wallet', on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    amount = models.FloatField()

    def as_dict(self):
        return {
            "id": self.id,
            "crypt": self.code,
            "amount": self.amount,
        }

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

    @staticmethod
    def create_ledger_record(wallet, action, targetCryp, pricePerc, quan):
        r = CryptoWalletLedger(cryptowallet=wallet, action_type=action, targetCrypto=targetCryp, pricePerCrypto=pricePerc, quantity=quan)
        return r


    def as_dict(self):
        return {
            "id": self.id,
            "action": self.action_type,
            "targetCrypto": self.targetCrypto,
            "price": self.pricePerCrypto,
            "quantity": self.quantity,
            "created": self.created,
        }