from django.db import models
from django.contrib.auth.models import AbstractUser
from financial_products.models import SavingProduct
from financial_products.models import DepositProduct

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=20)
    email = models.EmailField(max_length=30, blank=True, null=True)
    age = models.IntegerField(default=0)
    salary = models.IntegerField(default=0)
    wealth = models.IntegerField(default=0)
    monthly_deposit = models.IntegerField(default=0)
    desire_period = models.IntegerField(default=0)
    saving = models.ManyToManyField(SavingProduct, related_name='interested_users_saving')
    deposit = models.ManyToManyField(DepositProduct, related_name='interested_users_deposit')
