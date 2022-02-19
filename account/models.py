from django.db import models
from django.contrib.auth.models import AbstractUser
USER_TYPE_CHOICES = (
    ('student', 'student'),
    ('teacher', 'teacher'),
    ('staff', 'staff'),
    ('admin', 'admin'),
                    )
class User(AbstractUser):
    user_type = models.CharField(max_length=40,choices=USER_TYPE_CHOICES)

    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.wallet.points
        return 0