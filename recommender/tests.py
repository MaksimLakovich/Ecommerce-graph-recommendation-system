from rest_framework.test import APITestCase

from catalog.models import Aisle, Department, Product
from preferences.models import UserInteraction
from users.models import AppUser


class UserRecommendationsAPITestCase(APITestCase):
    """Базовые тесты API для получения рекомендаций пользователя."""

    def setUp(self):
        """Создаем пользователя, департамент, ряд и продукт."""
        self.user = AppUser.objects.create_user(
            email="testuser@example.com",
            password="password123"
        )
        self.department = Department.objects.create(dataset_department_id=1, department="Молочные")
        self.aisle = Aisle.objects.create(dataset_aisle_id=1, aisle="Молочные продукты")
        self.product = Product.objects.create(
            dataset_product_id=1,
            product_name="Молоко",
            aisle_id=self.aisle,
            department_id=self.department
        )

        # Логинимся как пользователь
        self.client.login(email="testuser@example.com", password="password123")

        # Добавим одно взаимодействие для имитации данных
        UserInteraction.objects.create(
            user_id=self.user,
            product_id=self.product,
            aisle_id=self.aisle,
            interaction_type="preference",
            source="explicit",
            weight=5.0
        )

    def test_get_recommendations(self):
        """Проверка получения рекомендаций через API."""
        response = self.client.get("/recommendations/api/recommendations/")
        self.assertEqual(response.status_code, 200)

        # Проверяем, что возвращается словарь с нужными ключами
        self.assertIsInstance(response.data, dict)
        self.assertIn("pagerank", response.data)
        self.assertIn("collaborative", response.data)
        self.assertIn("knn", response.data)


class StatisticsAPITestCase(APITestCase):
    """Базовые тесты API для получения статистики популярных продуктов и категорий."""

    def setUp(self):
        """Создаем пользователя, департамент, ряд, продукт и взаимодействие."""
        self.user = AppUser.objects.create_user(
            email="statsuser@example.com",
            password="password123"
        )
        self.department = Department.objects.create(dataset_department_id=1, department="Молочные")
        self.aisle = Aisle.objects.create(dataset_aisle_id=1, aisle="Молочные продукты")
        self.product = Product.objects.create(
            dataset_product_id=1,
            product_name="Молоко",
            aisle_id=self.aisle,
            department_id=self.department
        )

        # Логинимся
        self.client.login(email="statsuser@example.com", password="password123")

        # Создаем одно взаимодействие для статистики
        UserInteraction.objects.create(
            user_id=self.user,
            product_id=self.product,
            aisle_id=self.aisle,
            interaction_type="interaction",
            source="explicit",
            weight=5.0
        )

    def test_popular_products(self):
        """Проверка получения топ-10 популярных продуктов через API."""
        response = self.client.get("/recommendations/api/statistics/popular_products/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        if response.data:
            self.assertIn("product", response.data[0])
            self.assertIn("total_weight", response.data[0])

    def test_popular_aisles(self):
        """Проверка получения топ-5 популярных категорий (aisles) через API."""
        response = self.client.get("/recommendations/api/statistics/popular_aisles/")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        if response.data:
            self.assertIn("aisle", response.data[0])
            self.assertIn("total_weight", response.data[0])
