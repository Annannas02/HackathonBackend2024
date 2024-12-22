from rest_framework import generics
from subcategories import models, serializers
from rest_framework import generics

class SubcategoryList(generics.ListCreateAPIView):

    queryset = models.Categories.objects.all()
    serializer_class = serializers.SubcategorySerializer