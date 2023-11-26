from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import RecipeViewSet

router_v1 = DefaultRouter()

app_name = 'recipes'

router_v1.register(
    'recipes',
    RecipeViewSet,
    basename='recipes',
)

urlpatterns = [
    path('', include(router_v1.urls))
]
