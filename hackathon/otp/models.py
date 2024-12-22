from django.db import models
from users.models import User

class OTP(models.Model):
    personid = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()