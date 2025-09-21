# Загрузка данных в приложение Preferences

Приложение `preferences` поддерживает загрузку данных о взаимодействиях пользователей (implicit-события) из CSV-файлов сэмплов.  
Используются таблицы из датасета **Instacart Market Basket Analysis**:
- `order_products_all_sample.csv` — продукты в заказах пользователей (используется для implicit-событий: purchase, reorder).

Для удобной загрузки данных создан management command: `load_user_interaction_data.py`.

---

## 🚀 Запуск загрузки

1. Убедитесь, что применены миграции:
   ```commandline
   poetry run python manage.py migrate
   ```

2. Запустите команду для загрузки взаимодействий:
   ```commandline
   poetry run python manage.py load_user_interaction_data sample_data/order_products_all_sample.csv
   ```

---

## ⚙️ Особенности работы команды

- Используется transaction.atomic(), чтобы все операции выполнялись в одной транзакции.
- Если связанные объекты (AppUser, Order, Product) отсутствуют, строки пропускаются с сообщением об ошибке.
- Определяется тип взаимодействия:
  - `purchase`: первая покупка (weight = 1.0)
  - `reorder`: повторная покупка (weight = 2.0)
  - `preference`: явное предпочтение пользователя (weight = 5.0)
- Для явных предпочтений (aisle) product_id может быть Null.
- Используется get_or_create(), поэтому повторный запуск команды не создаст дубликаты.

---

## ⚠️ Примечания

- Все implicit-события автоматически получают source="implicit".
- Веса событий (weight) выставляются автоматически в зависимости от типа взаимодействия.
