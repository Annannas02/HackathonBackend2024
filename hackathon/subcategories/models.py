from django.db import models
from categories.models import Categories

class Subcategories(models.Model):
    name = models.CharField(max_length=50)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)