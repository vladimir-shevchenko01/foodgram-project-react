from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

from foodgram.settings import DEBUG, MEDIA_ROOT, MEDIA_URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('components.urls')),
    path('api/', include('users.urls')),
    path('api/', include('recipes.urls')),
]
if DEBUG:
    urlpatterns += static(MEDIA_URL,
                          document_root=MEDIA_ROOT)
