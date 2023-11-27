from rest_framework import viewsets

from components.models import Ingredient, Tag
from components.serializers import IngredientSerializer, TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    serializer_class = IngredientSerializer

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        search_name = self.request.query_params.get('name')
        if search_name is not None:
            queryset = queryset.filter(name__istartswith=search_name)
        return queryset
