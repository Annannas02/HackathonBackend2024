from rest_framework import serializers
from articles import models


class ArticlesSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category_id.name')
    subcategory = serializers.CharField(source='subcategory_id.name')

    class Meta:
        model = models.Articles
        exclude = ('id', )
        
    
class ArticleSelectionSerializer(serializers.Serializer):
    article_id = serializers.IntegerField()
    time_spent = serializers.IntegerField(min_value=0)  # Time in seconds