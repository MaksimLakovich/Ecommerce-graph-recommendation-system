from django.urls import path

from recommender.apps import RecommenderConfig
from recommender.views import (UserRecommendationsAPIView,
                               UserRecommendationsView, GenerateUserRecommendationsView)

app_name = RecommenderConfig.name


urlpatterns = [
    # Страница с рекомендациями (HTML)
    path("my/", UserRecommendationsView.as_view(), name="user_recommendations_page"),
    # API для получения рекомендаций в формате JSON
    path("api/recommendations/", UserRecommendationsAPIView.as_view(), name="user_recommendations_api"),
    path("generate/", GenerateUserRecommendationsView.as_view(), name="generate_user_recommendations"),
]
