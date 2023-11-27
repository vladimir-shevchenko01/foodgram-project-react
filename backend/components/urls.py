from django.urls import include, path
from rest_framework.routers import DefaultRouter

from components.views import IngredientViewSet, TagViewSet

router_v1 = DefaultRouter()

app_name = 'components'

router_v1.register(
    'tags',
    TagViewSet,
    basename='tags',
)
router_v1.register(
    'ingredients',
    IngredientViewSet,
    basename='recipe-ingredients'
)

urlpatterns = [
    path('', include(router_v1.urls))
]
