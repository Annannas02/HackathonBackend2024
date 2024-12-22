from django.db import models
from users.models import User
from articles.models import Articles

class Articlesession(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    article_id = models.ForeignKey(Articles, on_delete=models.CASCADE)
    time = models.DateTimeField()