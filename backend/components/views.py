from rest_framework import viewsets

from components.serializers import TagSerializer
from components.models import Tag


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
