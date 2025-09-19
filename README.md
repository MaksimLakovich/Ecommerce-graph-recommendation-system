# Graph-based Recommendation System for E-commerce

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
[5. Быстрый старт](#title5)  
[6. Документация](#title6)  
[7. Данные для исследования](#title7)  
[8. Roadmap](#title8)  
[9. Переменные окружения](#title9)  
[10. Автор](#title10)  

---

## <a id="title1"> 📌 О проекте </a>
Система рекомендаций для e-commerce, основанная на алгоритмах графов.  

1) Проект реализует три подхода к построению рекомендаций:
   - Алгоритм PageRank для оценки важности узлов (товаров).
   - Алгоритм коллаборативной фильтрации для рекомендаций на основе схожести пользователей (Collaborative Filtering).
   - Алгоритм нахождения ближайших соседей (k-Nearest Neighbors) для нахождения пользователей с похожими интересами.

2) Тестовые данные для БД взяты из публичного датасета [Instacart Market Basket Analysis](https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data).  
Детально описание как использовать тестовые данные в разделе <a id="title7"> Данные / Data </a>.

---

## <a id="title2"> ⚙️ Технологии </a>
- ***Backend***: Python, Django, Django REST Framework
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
├── .venv                # Виртуальное окружение poetry
├── config/              # Django проект и приложения
├── data/                # Исходные CSV из Kaggle (оригинальный датасет "Instacart Market Basket Analysis")
├── docs/                # Дополнительная документация по деталям (dataset_info.md, architecture.md, algorithms.md и т.д.)
├── sample_data/         # Уменьшенный датасет для теста и GitHub
├── users/               # Приложение проекта (клиенты)
├── recommendation/      # Приложение проекта (алгоритмы рекомендаций)
├── .env.example
├── .flake8
├── .gitignore
├── mypy.ini
├── poetry.lock
├── pyproject.toml
└── README.md
```

---

## <a id="title4"> 📊 API и функционал </a>

1. Добавление пользовательских взаимодействий
2. Получение рекомендаций (PageRank, CF, kNN)
3. Статистика и аналитика
4. Документация API (Swagger/ReDoc) будет доступна по адресу:
http://localhost:8000/api/docs/

---

## <a id="title5"> 🚀 Быстрый старт </a>
1. Клонировать репозиторий
    ```commandline
    git clone https://github.com/MaksimLakovich/Ecommerce-graph-recommendation-system.git
    cd Ecommerce-graph-recommendation-system
    ```

2. Запустить проект
    ```commandline
    docker-compose up --build
    ```

---

## <a id="title6"> 📖 Документация </a>

Подробное описание алгоритмов, архитектуры и процесса запуска находится в папке `docs/`.

---

## <a id="title7"> 🗂 Данные для исследования </a>

Проект поддерживает два варианта работы с данными из публичного датасета ["Instacart Market Basket Analysis" на платформе Kaggle](https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data):

1. **Быстрый запуск** — используйте готовые сэмплы в папке `sample_data/` (они уже включены в репозиторий).  
   Это самый простой способ сразу запустить сервис и протестировать функциональность.

2. **Полный датасет** — скачайте оригинальный датасет (объем данных ~700 MB и насчитывает миллионы записей) помещен в .gitignore и не загружался на репозиторий.  
   При желании, его можно скачать с Kaggle самостоятельно и распаковать в папку `data/` проекта с дальнейшей загрузкой в базу для полноценного эксперимента.

   

Подробная инструкция по скачиванию и подготовке данных: [docs/dataset_info.md](docs/dataset_info.md)

---

## <a id="title8"> 🛣 Roadmap </a>

- [x] Базовый API для рекомендаций
- [x] Интеграция Kaggle dataset
- [x] Алгоритмы PageRank / CF / kNN
- [ ] [Добавить Neo4j для больших графов](https://github.com/MaksimLakovich/Ecommerce-graph-recommendation-system/issues/3)
- [ ] Добавить Neo4j для больших графов
- [ ] A/B тестирование качества рекомендаций
- [ ] Визуализация графа (D3.js / Graphviz)
- [ ] Docker-образ для продакшн-сервера

---

## <a id="title9"> 🔑 Переменные окружения </a>

Все конфигурации проекта хранятся в файле `.env`.  
Пример файла доступен в репозитории как `.env.example`.

1. Скопируйте `.env.example` в `.env`:
   ```commandline
   cp .env.example .env
   ```
2. Укажите значения для переменных:

| Переменная | Описание                    | Пример                |
| ------- |-----------------------------|-----------------------|
| `DJANGO_SECRET_KEY` | Секретный ключ Django       | `django-insecure-...` |
| `DEBUG` | Режим отладки (True/False)  | `True`                |
| `DATABASE_NAME`      | Назване БД в PostgreSQL     | `<some_bd_name>`      |
| `DATABASE_PASSWORD` | Пароль к БД в PostgreSQL    | `<some_bd_password>`  |
| `DATABASE_HOST`           | Хост БД                     |                       |
| `DATABASE_PORT`           | Порт БД                     |                       |
| `ALLOWED_HOSTS` | Список хостов через запятую | `localhost,127.0.0.1` |
 


---

## <a id="title10"> 👨‍💻 Автор </a>

Разработано в рамках дипломного проекта.
 
**Автор**: Максим Лакович  
GitHub: [MaksimLakovich](https://github.com/MaksimLakovich)  
LinkedIn: [Maksim Lakovich](https://t.me/maksim_lakovich)  
Telegram: [@maksim_lakovich](https://t.me/maksim_lakovich)

---