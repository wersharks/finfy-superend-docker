from django.db import models
from django.contrib.auth import get_user_model
from annoying.fields import AutoOneToOneField
from enum import Enum
from .const import STOCK_MARKET
import yfinance as yf

User = get_user_model()

# class StocksBalance(models.Model):
#     code = models.CharField(max_length=5)
#     amount = models.FloatField()

# class StocksWallet(models.Model):
#     user = AutoOneToOneField(User, related_name='stocks', on_delete=models.CASCADE)
#     balance = models.ForeignKey(StocksBalance, null=True, on_delete=models.CASCADE)

#     def operate(self, stock_id, amount):
#         pass

#     def get_all_ledger(self):
#         data = {}

#         ledger = list(StocksWalletLedger.objects.filter(stockwallet=self))
#         if(len(ledger) <= 0):
#             data['code'] = -1
#             data['message'] = "no ledger record for your stocks"
#             return data

#         data['code'] = 1
#         data['data'] = []
#         for d in ledger:
#             data['data'].append(d.as_dict())
#         return data



# class ActionType(Enum):
#     BUY="buy"
#     SELL="sell"

# class StocksWalletLedger(models.Model):
#     stockwallet = models.ForeignKey(StocksWallet, related_name='ledger', on_delete=models.CASCADE)
#     action_type = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in ActionType])
#     targetStock = models.CharField(max_length=5,)
#     pricePerStock = models.FloatField()
#     quantity = models.PositiveIntegerField()

#     created = models.DateTimeField(auto_now_add=True)

#     def as_dict(self):
#         return {
#             "id": self.id,
#             "action": self.action_type,
#             "targetStock": self.targetStock,
#             "price": self.pricePerStock,
#             "quantity": self.quantity,
#             "created": self.created,
#         }


class StockWallet(models.Model):
    user = AutoOneToOneField(User, related_name='stocks', on_delete=models.CASCADE)

    def buy(self, stock_id, amount):
        data = {}
        if(not StockWallet.isValidStockId(stock_id)):
            data['code'] = -1
            data['message'] = "not a valid stock"
            return data
        
        price = StockWallet.get_stock_data(stock_id)
        if(amount * price > self.user.wallet.points):
            data['code'] = -1
            data['message'] = "not enough money for this transaction"
            return data

        # get all wallets with crypto_id
        bal = StockBalance.objects.filter(stockwallet=self, code=stock_id)
        if(bal.exists()):
            # Already wallet there so add some
            rc = bal[0]
            rc.amount += amount
            rc.save()
        else:
            # Create new wallet
            new_rc = StockBalance(stockwallet=self, code=stock_id, amount=amount)
            new_rc.save()

        self.user.wallet.operate(amount * price * -1)
        x = StockWalletLedger.create_ledger_record(self, ActionType.BUY, stock_id, price, amount)

        data['code'] = 1
        data['message'] = "Success"
        data['wallet'] = self.wallet_data()
        data['ledger'] = x.as_dict()
        return data

    def sell(self, stock_id, amount):
        data = {}
        if(not StockWallet.isValidStockId(stock_id)):
            data['code'] = -1
            data['message'] = "not a valid stock"
            return data
        
        price = StockWallet.get_stock_data(stock_id)

        # get all wallets with crypto_id
        bal = StockBalance.objects.filter(stockwallet=self, code=stock_id)
        if(not bal.exists() or not bal[0].amount>amount):
            data['code'] = -1
            data['message'] = "you don't have this stock for this transaction."
            return data
        
        r = bal[0]
        r.amount -= amount
        r.save()

        points = price * amount
        self.user.wallet.operate(points)

        x = StockWalletLedger.create_ledger_record(self, ActionType.SELL, stock_id, price, amount)

        data['code'] = 1
        data['message'] = "Success"
        data['wallet'] = self.wallet_data()
        data['ledger'] = x.as_dict()
        return data

    def wallet_data(self):
        data = list(StockBalance.objects.filter(stockwallet=self))
        if(len(data)>0):
            return [d.as_dict() for d in data]
        else:
            return {}

    def get_all_ledger(self):
        data = {}

        ledger = list(StockWalletLedger.objects.filter(stockwallet=self))
        if(len(ledger) <= 0):
            data['code'] = -1
            data['message'] = "no ledger record for your stock"
            return data

        data['code'] = 1
        data['data'] = []
        for d in ledger:
            data['data'].append(d.as_dict())
        return data

    @staticmethod
    def isValidStockId(id):
        if(id in STOCK_MARKET):
            return True
        else: return False

    @staticmethod
    def get_stock_data(stock_id):
        company_info = yf.Ticker(stock_id)
        hist = company_info.history(period="max")
        a = hist.to_numpy() 
        shape = a.shape
        end = shape[0]
        d = a[end-1][3]
        return d

class StockBalance(models.Model):
    stockwallet = models.ForeignKey(StockWallet, related_name='wallet', on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    amount = models.FloatField()

    def as_dict(self):
        return {
            "id": self.id,
            "stock": self.code,
            "amount": self.amount,
        }

class ActionType(Enum):
    BUY="buy"
    SELL="sell"

class StockWalletLedger(models.Model):
    stockwallet = models.ForeignKey(StockWallet, related_name='ledger', on_delete=models.CASCADE)
    action_type = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in ActionType])
    targetStock = models.CharField(max_length=5,)
    pricePerStock = models.FloatField()
    quantity = models.FloatField()

    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_ledger_record(wallet, action, targetStock, pricePerc, quan):
        r = StockWalletLedger(stockwallet=wallet, action_type=action.value, targetStock=targetStock, pricePerStock=pricePerc, quantity=quan)
        return r


    def as_dict(self):
        return {
            "id": self.id,
            "action": self.action_type,
            "targetStock": self.targetStock,
            "price": self.pricePerStock,
            "quantity": self.quantity,
            "created": self.created,
        }