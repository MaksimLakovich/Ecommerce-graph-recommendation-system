import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Aisle, Department, Product


class Command(BaseCommand):
    help = "Загрузить данные в БД (departments, aisles, products)"

    def add_arguments(self, parser):
        """Добавление аргументов "Тип данных (data_type)" и "Путь к файлу (csv_path)" в management/commands.
        Команды:
        - Загрузить департаменты:
            python manage.py load_catalog_data departments sample_data/departments_sample.csv
        - Загрузить ряды:
            python manage.py load_catalog_data aisles sample_data/aisles_sample.csv
        - Загрузить продукты:
            python manage.py load_catalog_data products sample_data/products_sample.csv
        """
        parser.add_argument(
            "data_type",
            type=str,
            choices=["departments", "aisles", "products"],
            help="Тип данных для загрузки",
        )
        parser.add_argument(
            "csv_path",
            type=str,
            help="Путь к CSV-файлу",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        data_type = options["data_type"]
        csv_path = options["csv_path"]

        self.stdout.write(f"Загружаем {data_type} из {csv_path}...")

        if data_type == "departments":
            self.load_departments(csv_path)
        elif data_type == "aisles":
            self.load_aisles(csv_path)
        elif data_type == "products":
            self.load_products(csv_path)

    def load_departments(self, csv_path):
        """Загрузка departments в БД PostgreSQL."""
        df = pd.read_csv(csv_path, usecols=["department_id", "department"])
        created_count = 0
        for _, row in df.iterrows():
            _, created = Department.objects.get_or_create(
                dataset_department_id=row["department_id"],
                defaults={
                    "department": row["department"]
                },
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Загружено {created_count} департаментов."))

    def load_aisles(self, csv_path):
        """Загрузка aisles в БД PostgreSQL."""
        df = pd.read_csv(csv_path, usecols=["aisle_id", "aisle"])
        created_count = 0
        for _, row in df.iterrows():
            _, created = Aisle.objects.get_or_create(
                dataset_aisle_id=row["aisle_id"],
                defaults={
                    "aisle": row["aisle"]
                },
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Загружено {created_count} рядов."))

    def load_products(self, csv_path):
        """Загрузка products в БД PostgreSQL."""
        df = pd.read_csv(csv_path, usecols=["product_id", "product_name", "aisle_id", "department_id"])
        created_count = 0
        for _, row in df.iterrows():
            aisle = Aisle.objects.get(dataset_aisle_id=row["aisle_id"])
            department = Department.objects.get(dataset_department_id=row["department_id"])
            _, created = Product.objects.get_or_create(
                dataset_product_id=row["product_id"],
                defaults={
                    "product_name": row["product_name"],
                    "aisle_id": aisle,
                    "department_id": department,
                },
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f"Загружено {created_count} продуктов."))
