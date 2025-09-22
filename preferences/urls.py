from django.urls import path

from preferences.apps import PreferencesConfig
from preferences.views import UserPreferencesView

app_name = PreferencesConfig.name


urlpatterns = [
    path("my/", UserPreferencesView.as_view(), name="user_preferences_page"),
]
