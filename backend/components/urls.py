from django.urls import include, path
from rest_framework.routers import DefaultRouter

from components.views import TagViewSet

router_v1 = DefaultRouter()

app_name = 'components'

router_v1.register(
    'tags',
    TagViewSet,
    basename='tags',
)

urlpatterns = [
    path('', include(router_v1.urls))
]
