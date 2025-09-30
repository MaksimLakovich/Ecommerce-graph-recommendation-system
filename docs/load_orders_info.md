# Загрузка данных в приложение Orders

Приложение `orders` поддерживает загрузку тестовых данных из CSV-файлов сэмплов.  
Используются таблицы из датасета **Instacart Market Basket Analysis**:

1. `orders_sample.csv` — заказы покупателя
2. `order_products_all_sample.csv` — продукты в заказе

Для удобной загрузки данных создан management command: `load_order_data.py`.

---

## 🚀 Запуск загрузки

1. Убедитесь, что у вас применены миграции:
   ```commandline
   poetry run python manage.py migrate
   ```


2. Запустите команду для загрузки Заказов:
   ```commandline
   python manage.py load_order_data orders sample_data/orders_sample.csv
   ```
   

3. Запустите команду для загрузки Продуктов в заказах:
   ```commandline
   python manage.py load_order_data order_products sample_data/order_products_all_sample.csv
   ```


Особенности:
- Команда использует transaction.atomic(), чтобы все операции были в одной транзакции.
- Если связанные объекты (AppUser, Order или Product) отсутствуют, строки пропускаются с сообщением об ошибке.
- Поддерживается корректная работа с NaN для поля days_since_prior_order.
- При повторном запуске уже существующие записи не дублируются (используется get_or_create).
- Поток работы загрузки

---

## ⚠️ Примечания

1. Используется get_or_create, поэтому повторный запуск команды не создаст дубликаты.


2. Синтаксис:
   ```bash
   python manage.py load_order_data <data_type> <csv_path>
   ```

   Аргументы команды:
   - `data_type` — тип данных (orders, order_products)
   - `csv_path` — путь к CSV-файлу

---
