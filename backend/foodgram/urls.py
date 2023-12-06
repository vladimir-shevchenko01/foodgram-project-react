from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from components.views import IngredientViewSet, TagViewSet
from foodgram.settings import DEBUG, MEDIA_ROOT, MEDIA_URL
from recipes.views import RecipeViewSet
from users.views import UserViewSet

router_v1 = DefaultRouter()

router_v1.register(
    'recipes',
    RecipeViewSet,
    basename='recipes',
)

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

router_v1.register(
    'users',
    UserViewSet,
    basename='users',
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router_v1.urls)),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken')),
]

if DEBUG:
    urlpatterns += static(MEDIA_URL,
                          document_root=MEDIA_ROOT)
