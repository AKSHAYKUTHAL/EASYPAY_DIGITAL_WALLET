from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    username = models.CharField(max_length=100)
    user_id = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(unique=True)
    is_email_verfied = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_2fa = models.BooleanField(default=False)
    otp = models.CharField(max_length=10,blank=True,null=True)
    total_transactions = models.IntegerField(default=0)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.username



