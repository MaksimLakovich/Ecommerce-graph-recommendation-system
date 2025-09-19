# Загрузка пользователей в БД

Для тестирования системы необходимо загрузить пользователей из датасета **Instacart Market Basket Analysis**.  
Мы используем `orders_sample.csv` и генерируем дополнительные данные (имя, фамилия, город, email) с помощью [Faker](https://faker.readthedocs.io/).

---

## 📌 Как это работает

- Каждый `user_id` из датасета - это отдельный объект `AppUser`.
- Для авторизации создаётся уникальный email вида `user<ID>@example.com`.
- Для всех пользователей устанавливается одинаковый пароль (по умолчанию: `123456qwe`).
- Faker генерирует `first_name`, `last_name`, `city`.

---

## 🚀 Запуск загрузки

1. Убедитесь, что у вас применены миграции:
   ```commandline
   poetry run python manage.py migrate
   ```

2. Запустите команду для загрузки пользователей:
   ```commandline
   poetry run python manage.py load_users sample_data/orders_sample.csv
   ```
   
3. В консоли появится информация о прогрессе:
   ```commandline
   Загружаем пользователей из sample_data/orders_sample.csv...
   Найдено 9542 уникальных пользователей
   Загружено 9542 пользователей
   ```