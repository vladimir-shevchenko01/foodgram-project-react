from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

app_name = 'users'

router_v1 = DefaultRouter()

router_v1.register(
    'users',
    UserViewSet,
    basename='users',
)
# router_v1.register(
#     'users/<int:pk>/subscribe/',
#     SubscribeViewSet,
#     basename='users',
# )


urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
# urlpatterns += [
#     path('users/<int:pk>/subscribe/',
#          SubscribeViewSet.as_view({'post': 'subscribe', 'delete': 'unsubscribe'}),
#          name='user-subscribe'

