from rest_framework.test import APITestCase

from preferences.models import Aisle, UserPreference
from users.models import AppUser


class UserPreferencesAPITestCase(APITestCase):
    """Базовые тесты API для добавления и получения предпочтений покупателя."""

    def setUp(self):
        """Создаем покупателя и несколько категорий (aisles)."""
        self.user = AppUser.objects.create_user(
            email="testuser@example.com",
            password="password123"
        )
        self.aisle1 = Aisle.objects.create(dataset_aisle_id=1, aisle="Молоко")
        self.aisle2 = Aisle.objects.create(dataset_aisle_id=2, aisle="Хлеб")
        self.client.login(email="testuser@example.com", password="password123")

    def test_create_preference(self):
        """Проверка создания предпочтения через API."""
        data = {"aisle_id": self.aisle1.id}
        response = self.client.post("/preferences/api/preferences/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(UserPreference.objects.count(), 1)

    def test_list_preferences(self):
        """Проверка получения списка предпочтений текущего пользователя через API.."""
        UserPreference.objects.create(user_id=self.user, aisle_id=self.aisle1)
        UserPreference.objects.create(user_id=self.user, aisle_id=self.aisle2)

        response = self.client.get("/preferences/api/preferences/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
