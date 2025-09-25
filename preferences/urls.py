from django.urls import path
from rest_framework.routers import DefaultRouter

from preferences.apps import PreferencesConfig
from preferences.views import UserPreferencesView, UserPreferencesViewSet

app_name = PreferencesConfig.name

router = DefaultRouter()
router.register(r"api/preferences", UserPreferencesViewSet, basename="user-preferences")


urlpatterns = [
    path("my/", UserPreferencesView.as_view(), name="user_preferences_page"),
] + router.urls
