from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class User(AbstractBaseUser):
    username = models.CharField(max_length=50,unique=True)
    password = models.CharField(max_length=30,null=False)

    USERNAME_FIELD='username'