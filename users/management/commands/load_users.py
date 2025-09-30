import pandas as pd
from django.core.management.base import BaseCommand
from faker import Faker

from users.models import AppUser


class Command(BaseCommand):
    help = "Загрузить покупателей в БД из orders_sample.csv."

    def add_arguments(self, parser):
        """Добавление аргументов "Путь к файлу (csv_path)" и "Пароль (--password)" для команды."""
        parser.add_argument(
            "csv_path",
            type=str,
            help="Путь к CSV-файлу с заказами (sample_data/orders_sample.csv).",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="123456qwe",
            help="Пароль по умолчанию для создаваемых покупателей, но его можно менять если указать в команде.",
        )

    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        password = options["password"]

        # Можно указать "ru_RU" для русскоязычных данных, но оставлю "en_US" так как сам датасет англоязычный
        # и пусть все тестовые данные в проекте будут однообразны
        fake = Faker("en_US")

        self.stdout.write(f"Загружаем покупателей из {csv_path}...")

        # Читаю orders_sample.csv - будем загружать сэмплы
        df = pd.read_csv(csv_path, usecols=["user_id"])

        # Оставляю только уникальные user_id
        user_ids = df["user_id"].unique()
        self.stdout.write(f"Найдено {len(user_ids)} уникальных покупателей.")

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

        self.stdout.write(self.style.SUCCESS(f"Загружено {created_count} покупателей."))
