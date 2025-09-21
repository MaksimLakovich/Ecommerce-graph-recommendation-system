# Загрузка данных в приложение Catalog

Приложение `catalog` поддерживает загрузку тестовых данных из CSV-файлов сэмплов.  
Используются таблицы из датасета **Instacart Market Basket Analysis**:

1. `departments_sample.csv` — департаменты
2. `aisles_sample.csv` — ряды/корзины
3. `products_sample.csv` — продукты

Для удобной загрузки данных создан management command: `load_catalog_data.py`.

---

## 🚀 Запуск загрузки

1. Убедитесь, что у вас применены миграции:
   ```commandline
   poetry run python manage.py migrate
   ```


2. Запустите команду для загрузки департаментов:
   ```commandline
   python manage.py load_catalog_data departments sample_data/departments_sample.csv
   ```
   - Что происходит: создаются записи в таблице Department с dataset_department_id и department.
   - В консоли появится информация о прогрессе:
     ```commandline
     Загружаем departments из sample_data/departments_sample.csv...
     Загружено 21 департаментов.
     ```


3. Далее запустите команду для загрузки рядов (aisles):
   ```commandline
   python manage.py load_catalog_data aisles sample_data/aisles_sample.csv
   ```
   - Что происходит: создаются записи в таблице Aisle с dataset_aisle_id и aisle.


4. Далее запустите команду для загрузки продуктов:
   ```commandline
   python manage.py load_catalog_data products sample_data/products_sample.csv
   ```
   - Что происходит: создаются записи в таблице Product с dataset_product_id, product_name, и связями через ForeignKey на Aisle и Department.

---

## ⚠️ Примечания

1. Для продуктов важно, чтобы ряды и департаменты были загружены перед загрузкой продуктов.


2. Используется get_or_create, поэтому повторный запуск команды не создаст дубликаты.


3. Синтаксис:
   ```bash
   python manage.py load_catalog_data <data_type> <csv_path>
   ```

   Аргументы команды:
   - `data_type` — тип данных (departments, aisles, products)
   - `csv_path` — путь к CSV-файлу
