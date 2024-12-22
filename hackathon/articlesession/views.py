from rest_framework import generics
from articlesession import models, serializers

class ArticlesessionList(generics.ListCreateAPIView):

    queryset = models.Articlesession.objects.all()
    serializer_class = serializers.ArticlesessionSerializer