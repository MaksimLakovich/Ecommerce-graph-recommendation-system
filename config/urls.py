from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Ecommerce graph recommendation system",
        default_version="v1",
        description="Документация к EGRS (Ecommerce graph recommendation system)",
        contact=openapi.Contact(email="maks_lakovich@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # namespace="users" это заданное пространство имен в "users/urls.py" с помощью "UsersConfig.name"
    path("users/", include("users.urls", namespace="users")),
    path("preferences/", include("preferences.urls", namespace="preferences")),
    path("recommendations/", include("recommender.urls", namespace="recommender")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
