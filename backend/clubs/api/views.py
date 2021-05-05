from rest_framework import viewsets

from .serializers import ClubSerializer
from ..models import Club


class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
