from rest_framework import serializers
from articlesession import models

class ArticlesessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Articlesession
        fields = '__all__'