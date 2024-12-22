from rest_framework import generics
from categories import models, serializers
from rest_framework import generics

class CategoryList(generics.ListCreateAPIView):

    queryset = models.Categories.objects.all()
    serializer_class = serializers.CategorySerializer