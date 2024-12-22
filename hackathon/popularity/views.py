from rest_framework import generics
from popularity import models, serializers
from rest_framework import generics

class PopularityList(generics.ListCreateAPIView):

    queryset = models.Popularity.objects.all()
    serializer_class = serializers.PopularitySerializer