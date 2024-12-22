from rest_framework import serializers
from popularity import models

class PopularitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Popularity
        fields = '__all__'