from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # namespace="users" это заданное пространство имен в "users/urls.py" с помощью "UsersConfig.name"
    path("users/", include("users.urls", namespace="users")),
    path("preferences/", include("preferences.urls", namespace="preferences")),
    path("recommendations/", include("recommender.urls", namespace="recommendations"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
