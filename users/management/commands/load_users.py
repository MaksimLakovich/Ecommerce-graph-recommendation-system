import pandas as pd
from faker import Faker

from users.models import AppUser

# Можно указать "ru_RU" для русскоязычных данных, но оставлю "en_US" так как сам датасет англоязычный
# и пусть все тестовые данные в проекте будут однообразны
fake = Faker("en_US")


def load_users_from_orders(csv_path: str, password: str = "123456qwe"):
    """Загрузка users в БД PostgreSQL."""
    print(f"Загружаем пользователей из {csv_path}...")

    # Читаю orders_sample.csv - будем загружать сэмплы
    df = pd.read_csv(csv_path, usecols=["user_id"])

    # Оставляю только уникальные user_id
    user_ids = df["user_id"].unique()
    print(f"Найдено {len(user_ids)} уникальных пользователей")

    created_count = 0

    for id in user_ids:
        # Формирую уникальный фейковый email, который нужен для правдоподобности процесса авторизации,
        # фиксации предпочтений и получении рекомендаций
        email = f"user{id}@example.com"
        # Создаю пользователя, если его еще нет
        user, created = AppUser.objects.get_or_create(
            dataset_user_id=id,
            defaults={
                "email": email,
                "password": password,  # Будет перезаписан set_password ниже
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "city": fake.city(),
            },
        )

        if created:
            user.set_password(password)
            user.save()
            created_count += 1

    print(f"Загружено {created_count} пользователей")
