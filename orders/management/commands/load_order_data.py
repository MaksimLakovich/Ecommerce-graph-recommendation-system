import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Product
from orders.models import Order, OrderProduct
from users.models import AppUser


class Command(BaseCommand):
    help = "Загрузить данные в БД (orders, order_products)"

    def add_arguments(self, parser):
        """Добавление аргументов "Тип данных (data_type)" и "Путь к файлу (csv_path)" для команды.
        Команды:
        - Загрузить заказы:
            python manage.py load_order_data orders sample_data/orders_sample.csv
        - Загрузить продукты в заказе:
            python manage.py load_order_data order_products sample_data/order_products_all_sample.csv
        """
        parser.add_argument(
            "data_type",
            type=str,
            choices=["orders", "order_products"],
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

        if data_type == "orders":
            self.load_orders(csv_path)
        elif data_type == "order_products":
            self.load_order_products(csv_path)

    def load_orders(self, csv_path):
        """Загрузка orders в БД PostgreSQL."""
        df = pd.read_csv(
            csv_path,
            usecols=[
                "order_id", "user_id", "order_number", "order_dow", "order_hour_of_day", "days_since_prior_order",
            ]
        )
        created_count = 0

        for row in df.itertuples(index=False):  # row.order_id, row.user_id, row.order_number и так далее
            try:
                user = AppUser.objects.get(dataset_user_id=row.user_id)
            except AppUser.DoesNotExist:
                self.stderr.write(f"Покупатель не найден: dataset_user_id={row.user_id} "
                                  f"поэтому пропускаем заказ id={row.order_id}")
                continue

            # Преобразую days_since_prior_order: NaN в None
            days = None
            if not pd.isna(row.days_since_prior_order):
                days = row.days_since_prior_order

            _, created = Order.objects.get_or_create(
                dataset_order_id=row.order_id,
                defaults={
                    "user_id": user,
                    "order_number": row.order_number,
                    "order_dow": row.order_dow,
                    "order_hour_of_day": row.order_hour_of_day,
                    "days_since_prior_order": days,
                },
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Загружено {created_count} заказов."))

    def load_order_products(self, csv_path):
        """Загрузка order_products в БД PostgreSQL."""

        skipped_orders = 0
        skipped_products = 0

        df = pd.read_csv(csv_path, usecols=["order_id", "product_id", "add_to_cart_order", "reordered"])
        created_count = 0
        for row in df.itertuples(index=False):
            # Ищу связанные объекты, если их нет то пропускаем
            try:
                order = Order.objects.get(dataset_order_id=row.order_id)
            except Order.DoesNotExist:
                self.stderr.write(f"Заказ не найден: dataset_order_id={row.order_id} поэтому пропускаем.")
                skipped_orders += 1
                continue

            try:
                product = Product.objects.get(dataset_product_id=row.product_id)
            except Product.DoesNotExist:
                self.stderr.write(f"Продукт не найден: dataset_product_id={row.product_id} поэтому пропускаем.")
                skipped_products += 1
                continue

            _, created = OrderProduct.objects.get_or_create(
                order_id=order,
                product_id=product,
                defaults={
                    "add_to_cart_order": row.add_to_cart_order,
                    "reordered": row.reordered,
                },
            )

            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Загружено {created_count} записей в OrderProduct."))
        self.stdout.write(f"Пропущено: {skipped_orders} строк (заказы), {skipped_products} строк (продукты)")
