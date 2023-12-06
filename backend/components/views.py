from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.filters import SearchFilter

from components.models import IngredientModel, TagModel
from components.serializers import IngredientSerializer, TagSerializer
from foodgram.permissions import IsAdminOrReadOnly


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = TagModel.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = IngredientModel.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny, )
    pagination_class = None
    filter_backends = (SearchFilter, )
    search_fields = ('^name', )
