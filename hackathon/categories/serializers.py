from rest_framework import serializers
from categories import models

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Categories
        fields = '__all__'