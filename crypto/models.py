from django.db import models
from django.contrib.auth import get_user_model

from enum import Enum
from annoying.fields import AutoOneToOneField
from datetime import datetime, timezone

User = get_user_model()

class CryptoWallet(models.Model):
    user = AutoOneToOneField(User, related_name='crypt', on_delete=models.CASCADE)

    def operate(self, crytpcode, amount):
        pass

    def get_all_my_ledger(self):
        pass