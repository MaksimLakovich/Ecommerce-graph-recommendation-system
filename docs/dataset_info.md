# 🗂 Описание таблиц/колонок в данных для исследования

---

## 📍 1. departments_sample.csv

Таблица со списком департаментов (более общая категория, чем aisle).

`department_id` — уникальный ID департамента.  
`department` — название департамента (например: "produce", "beverages").  

Пример:

| department\_id | department |
| -------------- | ---------- |
| 1              | produce    |
| 2              | beverages  |
| 3              | snacks     |

---

## 📍 2. aisles_sample.csv

Таблица со списком "корзин/рядов" (группировка товаров внутри департамента).

`aisle_id` — уникальный ID ряда (целое число).  
`aisle` — название ряда (например: "fresh vegetables", "canned soups").  

Пример:

| aisle_id | aisle            |
| -------- | ---------------- |
| 1        | fresh vegetables |
| 2        | packaged cheese  |
| 3        | canned soups     |

---

## 📍 3. products_sample.csv

Список всех продуктов. Каждый продукт привязан к aisle и department.

`product_id` — уникальный ID продукта.  
`product_name` — название продукта.  
`aisle_id` — внешний ключ - aisles.aisle_id.  
`department_id` — внешний ключ - departments.department_id.  

Пример:

| product\_id | product\_name                 | aisle\_id | department\_id |
| ----------- | ----------------------------- | --------- | -------------- |
| 1           | Chocolate Sandwich Cookies    | 61        | 19             |
| 2           | All-Seasons Salt              | 104       | 13             |
| 3           | Robust Golden Unsweetened Tea | 94        | 7              |

---

## 📍 4. orders_sample.csv

История заказов (кто и какой заказ сделал).

`order_id` — уникальный ID заказа.  
`user_id` — ID пользователя, сделавшего заказ.  
`eval_set` — набор данных, где заказ хранится (train, prior).  
`order_number` — номер заказа пользователя (1-й заказ, 2-й заказ и т.д.).  
`order_dow` — день недели (0 = воскресенье, 1 = понедельник и т.д.).  
`order_hour_of_day` — час заказа (например: 14 = 14:00).  
`days_since_prior_order` — сколько дней прошло с предыдущего заказа (может быть NaN для первого заказа).  

Пример:

| order\_id | user\_id | eval\_set | order\_number | order\_dow | order\_hour\_of\_day | days\_since\_prior\_order |
| --------- | -------- | --------- | ------------- | ---------- | -------------------- | ------------------------- |
| 1         | 112108   | train     | 4             | 4          | 10                   | 9                         |
| 2         | 17668    | prior     | 14            | 1          | 15                   | 30                        |

---

## 📍 5. order_products_all_sample.csv

Содержимое заказов (какие продукты были куплены).

`order_id` — ID заказа → orders.order_id.  
`product_id` — ID продукта → products.product_id.  
`add_to_cart_order` — порядок добавления товара в корзину.  
`reordered` — индикатор (1 = этот товар уже заказывался пользователем ранее, 0 = заказан впервые).  

Пример:

| order\_id | product\_id | add\_to\_cart\_order | reordered |
| --------- | ----------- | -------------------- | --------- |
| 1         | 49302       | 1                    | 1         |
| 1         | 11109       | 2                    | 1         |
| 2         | 10246       | 1                    | 0         |

---
