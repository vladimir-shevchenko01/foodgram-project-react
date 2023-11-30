from django.urls import include, path
from rest_framework.routers import DefaultRouter

from recipes.views import RecipeViewSet, AddOrDeleteFavoriteRecipe

router_v1 = DefaultRouter()

app_name = 'recipes'

router_v1.register(
    'recipes',
    RecipeViewSet,
    basename='recipes',
)



urlpatterns = [
    path('', include(router_v1.urls)),
    # path('recipes/<int:recipe_id>/favorite/',
    #      AddOrDeleteFavoriteRecipe.as_view(actions={'post': 'create', 'delete': 'destroy'}), name='add_or_delete_favorite_recipe'),
]
