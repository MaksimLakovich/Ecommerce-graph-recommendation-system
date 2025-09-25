from django.urls import path
from rest_framework.routers import DefaultRouter

from recommender.apps import RecommenderConfig
from recommender.views import (GenerateUserRecommendationsView,
                               RecommendationStatisticsView,
                               UserRecommendationsView,
                               UserRecommendationsViewSet)

app_name = RecommenderConfig.name

router = DefaultRouter()
router.register(r"api/recommendations", UserRecommendationsViewSet, basename="user-recommendations")

urlpatterns = [
    path("my/", UserRecommendationsView.as_view(), name="user_recommendations_page"),
    path("generate/", GenerateUserRecommendationsView.as_view(), name="generate_user_recommendations"),
    path("statistics/", RecommendationStatisticsView.as_view(), name="recommendation_statistics_page"),
] + router.urls
