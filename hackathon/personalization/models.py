from django.db import models
from users.models import User
from subcategories.models import Subcategories

class Personalization(models.Model):
    value = models.PositiveIntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(Subcategories, on_delete=models.CASCADE)
