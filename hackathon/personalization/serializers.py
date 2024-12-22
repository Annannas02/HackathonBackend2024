from rest_framework import serializers
from personalization import models

class PersonalizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Personalization
        fields = '__all__'