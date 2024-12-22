from django.db import models
from articles.models import Articles

class Popularity(models.Model):
    value = models.PositiveIntegerField()
    article_id = models.ForeignKey(Articles, on_delete=models.CASCADE)