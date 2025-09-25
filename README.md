# Ecommerce Graph Recommendation System

# Система рекомендаций на основе графов для e-commerce

---

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.x-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.3-blue.svg)
![Redis](https://img.shields.io/badge/Redis-cache-red.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![Languages](https://img.shields.io/github/languages/top/MaksimLakovich/Ecommerce-graph-recommendation-system)

![CI](https://img.shields.io/github/actions/workflow/status/MaksimLakovich/Ecommerce-graph-recommendation-system/deploy.yml)
![Build Status](https://img.shields.io/github/actions/workflow/status/MaksimLakovich/Ecommerce-graph-recommendation-system/ci.yml)
![Last commit](https://img.shields.io/github/last-commit/MaksimLakovich/Ecommerce-graph-recommendation-system)
![Open Pull Requests](https://img.shields.io/github/issues-pr/MaksimLakovich/Ecommerce-graph-recommendation-system)
![Stars](https://img.shields.io/github/stars/MaksimLakovich/Ecommerce-graph-recommendation-system)

---

[1. О проекте](#title1)  
[2. Технологии](#title2)   
[3. Структура репозитория](#title3)   
[4. API и функционал](#title4)  
[5. Переменные окружения](#title5)  
[6. Быстрый старт](#title6)  
[7. Документация](#title7)  
[8. Данные для исследования](#title8)  
[9. Roadmap](#title9)  
[10. Автор](#title10)  

---

## <a id="title1"> 📌 О проекте </a>
Рекомендательная система для e-commerce, основанная на графовых алгоритмах.  

1) Проект реализует три подхода к построению рекомендаций:
   - Алгоритм ***PageRank*** для оценки важности узлов (товаров).
   - Алгоритм коллаборативной фильтрации для рекомендаций на основе схожести пользователей (***Collaborative Filtering***).
   - Алгоритм нахождения ближайших соседей (***k-Nearest Neighbors***) для нахождения пользователей с похожими интересами.


2) Тестовые данные для БД взяты из публичного датасета [Instacart Market Basket Analysis](https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data).  
Детально описание как использовать тестовые данные в разделе [Данные для исследования](#title8).

---

## <a id="title2"> ⚙️ Технологии </a>
- ***Backend***: Python, Django, Django REST Framework, Faker
- ***База данных***: PostgreSQL
- ***Кэширование***: Redis
- ***Графовые алгоритмы***: NetworkX
- ***Frontend***: HTML, CSS, Bootstrap
- ***Инфраструктура***: Docker, Docker Compose, CI/CD через GitHub Actions
- ***Качество кода***: PEP8, pre-commit hooks (flake8, black, mypy), тесты

---

## <a id="title3"> 📂 Структура репозитория </a>
```bash
.
├── .venv                                            # Виртуальное окружение poetry
├── config/                                          # Django проект и приложения, настройки
├── data/                                            # Исходные CSV из Kaggle (оригинальный датасет "Instacart Market Basket Analysis")
├── docs/                                            # Дополнительная документация по деталям (dataset_load_info.md, architecture.md, algorithms.md и т.д.)
├── sample_data/                                     # Уменьшенный датасет для теста и GitHub
│    ├── make_samples.py                             #
│    ├── update_order_products_all_sample.py         #
│    └── csv-files                                   # Полученные уменьшенные датасеты
├── users/                                           # Приложение проекта (клиенты)
│    ├── management/
│    │    └── commands/
│    │          └── load_users.py                    # Загрузка уменьшенного датасета (.csv) в БД
│    ├── templates/
│    │    └── users/
│    │          ├── base.html
│    │          ├── menu.html
│    │          └── login.html
│    ├── admin.py
│    ├── managers.py      # create_user(), create_superuser()
│    ├── models.py        # AppUser(AbstractUser)
│    ├── forms.py         # AppUserLoginForm(AuthenticationForm): Форма для входа ранее зарегистрированного пользователя в приложение
│    ├── urls.py          # "login/", "logout/"
│    └── views.py         # UserLoginView(LoginView): Представление для входа пользователя (login.html)
├── catalog/                                         # Приложение проекта (каталог продуктов)
│    ├── management/
│    │    └── commands/
│    │          └── load_catalog_data.py             # Загрузка уменьшенного датасета (.csv) в БД
│    ├── admin.py
│    ├── models.py
│    └── ...
├── orders/                                          # Приложение проекта (заказы)
│    ├── management/
│    │    └── commands/
│    │          └── load_orders_data.py              # Загрузка уменьшенного датасета (.csv) в БД
│    ├── admin.py
│    ├── models.py
│    └── ...
├── preferences/                                     # Приложение проекта (предпочтения)
│    ├── management/
│    │    └── commands/
│    │          └── load_user_interaction_data.py    # Загрузка уменьшенного датасета (.csv) в БД
│    ├── templates/
│    │    └── preferences/
│    │          └── user_preferences.html
│    ├── admin.py
│    ├── models.py        # UserInteraction(models.Model), UserPreference(models.Model)
│    ├── serializers.py   # UserPreferenceSerializer для осуществления базовой сериализация в DRF
│    ├── signals.py       # Сигнал об изменении в UserInteraction для сброса кэша
│    ├── forms.py         # UserPreferencesForm(forms.Form): Форма выбора явных предпочтений покупателем (товарные категории)
│    ├── tests.py
│    ├── urls.py          # "my/"  + API
│    └── views.py         # UserPreferencesView(LoginRequiredMixin, FormView): Страница "Мои предпочтения" с выбором товарных предпочтений покупателем / UserPreferencesViewSet(viewsets.ModelViewSet) - API-вью 
├── recommender/                                     # Приложение проекта (алгоритмы рекомендаций)
│    ├── algorithms/
│    │    ├── pagerank.py            # Алгоритм PageRank для оценки важности узлов
│    │    ├── collaborative.py       # Алгоритм Collaborative Filtering (коллаборативная фильтрация) для рекомендаций на основе схожести пользователей
│    │    └── knn.py                 # Алгоритм k-Nearest Neighbors для нахождения ближайших соседей для нахождения пользователей с похожими интересами
│    ├── templates/
│    │    └── recommender/
│    │          └── user_recommendations.html
│    ├── services.py      # Сервисы для получения рекомендаций (интеграция всх трех алгоритмов воедино)
│    ├── serializers.py   # UserRecommendationsSerializer для представления рекомендаций пользователя по трем алгоритмам (PP, CF, nKK) в DRF / Сериализаторы для статистики
│    ├── tests.py
│    ├── urls.py          # "my/", "generate/"  + API
│    └── views.py         # UserRecommendationsView(LoginRequiredMixin, TemplateView): отображения страницы "Рекомендации для меня" / UserRecommendationsViewSet(viewsets.ViewSet): DRF-вью для работы с рекомендациями
├── .env.example
├── .flake8
├── .gitignore
├── mypy.ini
├── poetry.lock
├── pyproject.toml
├── static
├── staticfiles
└── README.md
```

---

## <a id="title4"> 📊 API и функционал </a>

1. **Авторизация пользователей (login/logout)**:
   - Вход в систему (login) через форму логина в Django - `AuthenticationForm`.
   - Выход из системы (logout).
   - После успешного входа идет переход на страницу "Мои предпочтения".
   - Используется кастомная модель `AppUser`.
2. Алгоритмы для поиска рекомендаций: PageRank, CF, kNN.
3. **Автоматически**: Автоматизировано добавление пользовательских взаимодействий на основе истории покупок (первая покупка товара, повторная и т.д).
4. Статистика и аналитика.
5. **Страница "Мои предпочтения"**: интерфейс для ввода и хранения пользовательских предпочтений.
6. **Страница "Рекомендации для меня"**: интерфейс для просмотра персонализированных рекомендаций для покупателя на основе его UserInteraction и на базе графовых алгоритмов.
7. **Страница "Статистика"**: интерфейс для просмотра самых популярных товаров среди всех.
8. Документация API (Swagger/ReDoc) будет доступна по адресу:  
   
    ***Документация***
   - Swagger UI: http://127.0.0.1:8000/swagger/
   - Redoc: http://127.0.0.1:8000/redoc/

   ***Кратко про API:***
   - `API для предпочтений`: Пользователи могут управлять своими предпочтениями через API с использованием Django REST Framework.  
   Эндпоинт: http://127.0.0.1:8000/preferences/api/preferences/
   - `API для рекомендаций`: Пользователи могут получать рекомендации для них через API с использованием Django REST Framework.  
   Эндпоинт: http://127.0.0.1:8000/recommendations/api/recommendations/
   - `API для статистики`: Пользователи могут получать статистику с самыми популярными продуктами и категориями среди всех покупателей через API с использованием Django REST Framework.  
   Эндпоинты:  
   http://127.0.0.1:8000/recommendations/api/statistics/popular_products/  
   http://127.0.0.1:8000/recommendations/api/statistics/popular_aisles/  

---

## <a id="title5"> 🔑 Переменные окружения </a>

Все конфигурации проекта хранятся в файле `.env`.  
Пример файла доступен в репозитории как `.env.example`.

1. Скопируйте `.env.example` в `.env`:
   ```commandline
   cp .env.example .env
   ```
2. Укажите значения для переменных:

| Переменная | Описание                   | Пример                |
| ------- |----------------------------|-----------------------|
| `DJANGO_SECRET_KEY` | Секретный ключ Django      | `django-insecure-...` |
| `DEBUG` | Режим отладки (True/False) | `True`                |
| `DATABASE_NAME`      | Назване БД в PostgreSQL    | `<some_bd_name>`      |
| `DATABASE_PASSWORD` | Пароль к БД в PostgreSQL   | `<some_bd_password>`  |
| `DATABASE_HOST`           | Хост БД                    |                       |
| `DATABASE_PORT`           | Порт БД                    |                       |
| `REDIS_URL`           | Порт Redis-сервера         | `<.../1>`                    |
| `ALLOWED_HOSTS` | Список хостов через запятую | `localhost,127.0.0.1` |

---

## <a id="title6"> 🚀 Быстрый старт (локально) </a>
1. Клонировать репозиторий
    ```commandline
    git clone https://github.com/MaksimLakovich/Ecommerce-graph-recommendation-system.git
    cd Ecommerce-graph-recommendation-system
    ```

2. Установить зависимости:
    ```commandline
    pip install --upgrade pip
    pip install -r requirements.txt
    ```

3. Настроить переменные окружения:
    ```commandline
    cp .env.example .env
    ```

4. Затем откройте .env и укажите значения для:
    ```commandline
    DJANGO_SECRET_KEY
    DEBUG
    DATABASE_NAME, DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT
    REDIS_URL
    ALLOWED_HOSTS
    ```

5. Применить миграции и создать суперпользователя:
    ```commandline
    python manage.py migrate
    python manage.py createsuperuser
    ```

6. Запустить сервер:
    ```commandline
    python manage.py runserver
    ```

После этого сервис будет доступен по адресу: http://127.0.0.1:8000/

---

## <a id="title7"> 📖 Документация </a>

Подробное описание алгоритмов, архитектуры и процесса запуска находится в папке `docs/`.  

Приложение `users`:
- [Users (app_users_info.md)](docs/app_users_info.md): описание модели, админки, кастомной команды для создания новых пользователей.
- [Загрузка пользователей (load_users_info.md)](docs/load_users_info.md): описание как загрузить в БД покупателей из датасета (сэмпла).

Приложение `catalog`:
- [Catalog (app_catalog_info.md)](docs/app_catalog_info.md): описание моделей, админок.
- [Загрузка каталога продуктов (load_catalog_info.md)](docs/load_catalog_info.md): описание как загрузить в БД продуктовые департаменты, ряды и сами продукты из датасета (сэмпла).

Приложение `orders`:
- [Orders (app_orders_info.md)](docs/app_orders_info.md): описание моделей, админок.
- [Загрузка заказов и их корзины (load_orders_info.md)](docs/load_orders_info.md): описание как загрузить в БД заказы покупателе и состав этих заказов (продукты в заказе) из датасета (сэмпла).

Приложение `preferences`:
- [Preferences (app_preferences_info.md)](docs/app_preferences_info.md): описание моделей, админок.
- [Загрузка предпочтений покупателя (load_preferences_info.md)](docs/load_preferences_info.md): описание как загрузить в БД явные и неявные предпочтения покупателей.
- [Страница "Мои предпочтения" (preferences_ui_info.md)](docs/preferences_ui_info.md): описание страницы "Мои предпочтения".

Приложение `recommender`:
- [Recommender (app_recommender_info.md)](docs/app_recommender_info.md): описание графовых алгоритмов.

---

## <a id="title8"> 🗂 Данные для исследования </a>

Проект поддерживает два варианта работы с данными из публичного датасета ["Instacart Market Basket Analysis" на платформе Kaggle](https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data):

1. **Быстрый запуск** — используйте готовые сэмплы в папке `sample_data/` (они уже включены в репозиторий).  
   Это самый простой способ сразу запустить сервис и протестировать функциональность.

2. **Полный датасет** — скачайте оригинальный датасет (объем данных ~700 MB и насчитывает миллионы записей) помещен в .gitignore и не загружался на репозиторий.  
   При желании, его можно скачать с Kaggle самостоятельно и распаковать в папку `data/` проекта с дальнейшей загрузкой в базу для полноценного эксперимента.

Подробное описание структуры данных в датасета (таблицы, колонки): [Описание датасета](docs/dataset_info.md)

Подробная инструкция по скачиванию и подготовке данных: [Загрузка датасета](docs/dataset_load_info.md)

---

## <a id="title9"> 🛣 Roadmap </a>

#### MVP (minimum viable product):
- [x] Приложения проекта (модели, админки, вью, маршруты)
- [x] Интеграция Kaggle dataset
- [x] Создание сэмплов из оригинального датасета и загрузка данных в БД
- [x] Добавить авторизацию в системе по email (login / logout)
- [x] Интерфейс взаимодействия с покупателем (возможность ввода и просмотра предпочтений)
- [x] API для предпочтений (эндпоинты для добавления предпочтений)
- [x] Алгоритмы PageRank / CF / kNN на основе графового представления
- [x] Интерфейс взаимодействия с покупателем (кнопка для получения рекомендаций / веб-страница для отображения рекомендаций пользователю)
- [X] API для рекомендаций (эндпоинты для получения рекомендаций)
- [x] Статистика и аналитика (страница для отображения статистики рекомендаций и популярности элементов)
- [X] API для рекомендаций (эндпоинты для получения статистики)
- [X] Документация (оформить инструкцию по запуску сервиса и взаимодействию с проектом в README файле)
- [X] Тестирование (написание базовых тестов для проверки API)

#### Будущие доработки (развитие системы):
- [ ] CI/CD для продакшн-сервера
- [ ] Усовершенствовать алгоритмы CF (сейчас это реализовано как "бипартитный граф") и kNN (сейчас это реализовано как "граф схожести") - можно убрать графовое представление в этих алгоритмах, заменив их на ***Машинное обучение (Machine LearningL)*** (библиотека Scikit-learn)
- [ ] Добавить Neo4j для больших графов
- [ ] A/B тестирование качества рекомендаций
- [ ] Визуализация графа (D3.js / Graphviz)

---

## <a id="title10"> 👨‍💻 Автор </a>

Разработано в рамках дипломного проекта.
 
**Автор**: Максим Лакович  
GitHub: [MaksimLakovich](https://github.com/MaksimLakovich)  
LinkedIn: [Maksim Lakovich](https://t.me/maksim_lakovich)  
Telegram: [@maksim_lakovich](https://t.me/maksim_lakovich)

---