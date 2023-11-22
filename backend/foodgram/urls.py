from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
]

z = {
    "username": "v",
    "first_name": "v",
    "last_name": "v",
    "email": "example@email.com",
    "password": "v"
}