# 📦 Приложение Catalog

Приложение `catalog` отвечает за хранение информации о товарах, рядах (aisles) и департаментах (departments).  
Это база для построения графа рекомендаций и работы с каталогом товаров.

---

## 🗂 Модели

### 1. Department
- **Описание:** Департамент — более общая категория товаров.  
- **Колонки:**
  - `dataset_department_id` — ID департамента из исходного датасета (уникальный, индексированный).
  - `department` — название департамента.
- **Примечание:** Используется для связи с продуктами и рядами.

### 2. Aisle
- **Описание:** Ряд или корзина — подкатегория внутри департамента.  
- **Колонки:**
  - `dataset_aisle_id` — ID ряда из датасета (уникальный, индексированный).
  - `aisle` — название ряда.
- **Примечание:** Связан с продуктами через ForeignKey.

### 3. Product
- **Описание:** Продукт, привязанный к ряду и департаменту.  
- **Колонки:**
  - `dataset_product_id` — ID продукта из датасета (уникальный, индексированный).
  - `product_name` — название продукта.
  - `aisle_id` — связь с объектом Aisle.
  - `department_id` — связь с объектом Department.

---

## 🖥 Админка

### Department
- `list_display`: `id`, `dataset_department_id`, `department`
- `list_filter`: `department`
- `search_fields`: `dataset_department_id`, `department`

### Aisle
- `list_display`: `id`, `dataset_aisle_id`, `aisle`
- `list_filter`: `aisle`
- `search_fields`: `dataset_aisle_id`, `aisle`

### Product
- `list_display`: `id`, `dataset_product_id`, `product_name`, `aisle_id`, `department_id`
- `list_filter`: `product_name`, `aisle_id`, `department_id`
- `search_fields`: `dataset_product_id`, `product_name`, `aisle_id`, `department_id`

---

## ⚠️ Примечания

1. Все связи построены через ForeignKey (`Product` → `Aisle`, `Product` → `Department`).  
2. Каждая модель хранит `dataset_id` из исходного CSV, что упрощает загрузку и проверку данных.
