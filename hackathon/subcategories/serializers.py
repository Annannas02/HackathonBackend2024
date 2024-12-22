from rest_framework import serializers
from subcategories import models

class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subcategories
        fields = '__all__'