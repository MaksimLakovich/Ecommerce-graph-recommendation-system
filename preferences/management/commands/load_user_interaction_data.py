import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction

from catalog.models import Product
from orders.models import Order
from preferences.models import UserInteraction


class Command(BaseCommand):
    help = ("Загрузить данные о взаимодействиях пользователей в части implicit-событий (т.е. данные, "
            "из истории покупок пользователя в таблице order_products_all_sample.csv (purchase, reorder)")

    def add_arguments(self, parser):
        """Добавление аргумента "Путь к файлу (csv_path)" для команды."""
        parser.add_argument(
            "csv_path",
            type=str,
            help="Путь к CSV-файлу",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        self.stdout.write(f"Загружаем взаимодействия покупатели из {csv_path}...")
        self.load_user_interaction(csv_path)

    def load_user_interaction(self, csv_path: str):
        """Загрузка UserInteraction в БД PostgreSQL."""
        df = pd.read_csv(
            csv_path,
            usecols=["order_id", "product_id", "add_to_cart_order", "reordered"]
        )

        created_count = 0
        skipped_count = 0

        for row in df.itertuples(index=False):  # row.order_id, row.product_id, row.add_to_cart_order, row.reordered
            # Явно привожу к int, чтоб убрать ошибку, которую MYPY выбрасывает потом при проверке
            order_id: int = int(row.order_id)  # type: ignore[arg-type]
            product_id: int = int(row.product_id)  # type: ignore[arg-type]

            try:
                order = Order.objects.get(dataset_order_id=order_id)
            except Order.DoesNotExist:
                self.stderr.write(f"Заказ не найден: dataset_order_id={row.order_id} и поэтому пропускаем.")
                skipped_count += 1
                continue

            # Получаю связанный объект "Покупатель" (order.user_id это уже объект AppUser)
            user = getattr(order, "user_id", None)
            if user is None:
                self.stderr.write(f"Заказ {order.dataset_order_id} не содержит user_id - поэтому пропускаем.")
                skipped_count += 1
                continue

            try:
                product = Product.objects.get(dataset_product_id=product_id)
            except Product.DoesNotExist:
                self.stderr.write(f"Продукт не найден: dataset_product_id={row.product_id}, поэтому пропускаем.")
                skipped_count += 1
                continue

            # Далее необходимо определить тип взаимодействия и его вес:
            # if self.interaction_type == "purchase":
            #     self.weight = 1.0
            # elif self.interaction_type == "reorder":
            #     self.weight = 2.0
            # elif self.interaction_type == "preference":
            #     self.weight = 5.0

            # Так как у нас в датасете есть только "выполненные заказы" с признаком "0-первая_покупка / 1-повторная",
            # то делаем так: если первая то просто purchase, если повторная то reorder
            reordered_value = getattr(row, "reordered", 0)
            if reordered_value == 1:
                interaction_type = "reorder"
                weight = 2.0
            else:
                interaction_type = "purchase"
                weight = 1.0

            # Создаём запись (aisle_id = None для implicit-событий потому что это будет для explicit-событий)
            # Можно использовать create, но нам нужно избегать дубликатов и поэтому делаю с get_or_create
            obj, created = UserInteraction.objects.get_or_create(  # type: ignore[attr-defined]
                user_id=user,
                product_id=product,
                interaction_type=interaction_type,
                source="implicit",
                defaults={
                    "aisle_id": None,
                    "weight": weight,
                },
            )
            if created:
                created_count += 1
            # ну а если не created, то это уже существующая запись и мы пропускаем ее (не дублируем)

        self.stdout.write(self.style.SUCCESS(f"ИТОГ: создано {created_count}, пропущено: {skipped_count}."))
