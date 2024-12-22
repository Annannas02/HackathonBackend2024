from django.db import models
from categories.models import Categories
from subcategories.models import Subcategories

class Articles(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200)
    publish_date = models.DateTimeField()
    modify_date = models.DateTimeField()
    summary = models.CharField(max_length=1000)
    category_id = models.ForeignKey(Categories, on_delete=models.CASCADE)
    subcategory_id = models.ForeignKey(Subcategories, on_delete=models.CASCADE)