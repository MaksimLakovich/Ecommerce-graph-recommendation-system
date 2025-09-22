# 👤 Пользователи системы

В проекте используется **кастомная модель пользователя** (`AppUser`), которая заменяет стандартного `User` в Django.

---

## 🔑 Основные особенности

- Авторизация по **email** (поле `username` удалено).
- Поддержка обычных пользователей (клиентов) и сотрудников (админов) через роли (`is_staff`, `is_superuser`).
- Возможность расширения профиля: имя, фамилия, город, аватар.
- Используется кастомный менеджер `UserManager` для создания пользователей и суперпользователей.

---
## 📲 Авторизация

Реализована через встроенные механизмы Django:
- Форма входа: `AppUserLoginForm` (`users/forms.py`).
- Вью: `UserLoginView` (`users/views.py`).
- Шаблоны:
  - `login.html` — форма входа.
  - `base.html` — общий шаблон с подключением Bootstrap.
  - `menu.html` — меню с login/logout.
- После входа → перенаправление на страницу `Мои предпочтения`.

**Маршруты (`users/urls.py`):**
- `/login/` → страница входа
- `/logout/` → выход из системы

**Настройки (`config/settings.py`):**
```python
LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'preferences:user_preferences'
LOGOUT_REDIRECT_URL = 'users:login'
```

---

## 🗂 Модель `AppUser` в users/models.py

| Поле       | Тип         | Описание                             |
| ---------- | ----------- | ------------------------------------ |
| `dataset_user_id`    | IntegerField  | ID пользователя в датасете |
| `email`    | EmailField  | Уникальный логин (используется как username) |
| `first_name` | CharField | Имя пользователя (опционально)       |
| `last_name`  | CharField | Фамилия пользователя (опционально)   |
| `city`     | CharField   | Город проживания (опционально)       |
| `avatar`   | ImageField  | Аватар (опционально)                 |
| `is_active`   | Boolean  | Активен ли пользователь              |
| `is_staff`    | Boolean  | Может ли войти в админку             |
| `is_superuser`| Boolean  | Полные права администратора          |
| `date_joined` | DateTime | Дата регистрации                     |
| `last_login`  | DateTime | Дата последнего входа                |

---

## ⚙️ Менеджер `UserManager` в users/managers.py

Кастомный менеджер для работы с пользователями.

### Методы
- `create_user(email, password, **extra_fields)` — создание обычного пользователя.
- `create_superuser(email, password, **extra_fields)` — создание суперпользователя.

> ⚠️ Валидация: Email и пароль обязательны.

---

## 🖥 Админка `AppUserAdmin` в users/admin.py

В административной панели реализованы:
- Список пользователей с полями: email, имя, фамилия, роли.
- Поиск по email, имени и фамилии.
- Фильтрация по статусам (`is_staff`, `is_active`).
- Редактирование профиля (имя, фамилия, город, аватар).
- Управление правами доступа.

---

## 📌 Пример использования

Создание суперпользователя
```commandline
python manage.py createsuperuser
```