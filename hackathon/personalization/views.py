from rest_framework import generics
from personalization import models, serializers

class PersonalizationList(generics.ListCreateAPIView):

    queryset = models.Personalization.objects.all()
    serializer_class = serializers.PersonalizationSerializer