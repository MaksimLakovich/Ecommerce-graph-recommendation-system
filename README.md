# Graph-based Recommendation System for E-commerce

## Система рекомендаций на основе графов для e-commerce

---

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.x-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.3-blue.svg)
![Redis](https://img.shields.io/badge/Redis-cache-red.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)
![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)
![CI](https://img.shields.io/github/actions/workflow/status/username/repo/deploy.yml)


![Build Status](https://img.shields.io/github/actions/workflow/status/user/repo/ci.yml)
![Last commit](https://img.shields.io/github/last-commit/user/repo)
![Issues](https://img.shields.io/github/issues/user/repo)
![Languages](https://img.shields.io/github/languages/top/user/repo)
![Stars](https://img.shields.io/github/stars/user/repo)

---

[1. О проекте](#title1) / 
[2. Технологии](#title2) / 
[3. Структура репозитория](#title3) / 
[4. API и функционал](#title4) / 
[5. Быстрый старт](#title5) / 
[6. Документация](#title6) / 
[7. Автор](#title7) / 

---

### <a id="title1"> 📌 О проекте </a>
Система рекомендаций для e-commerce, основанная на алгоритмах графов.  

1) Проект реализует три подхода к построению рекомендаций:
   - Алгоритм PageRank для оценки важности узлов (товаров).
   - Алгоритм коллаборативной фильтрации для рекомендаций на основе схожести пользователей (Collaborative Filtering).
   - Алгоритм нахождения ближайших соседей (k-Nearest Neighbors) для нахождения пользователей с похожими интересами.

2) Тестовые данные для БД взяты из публичного датасета [Instacart Market Basket Analysis](https://www.kaggle.com/datasets/psparks/instacart-market-basket-analysis/data).

---

### <a id="title2"> ⚙️ Технологии </a>
- ***Backend***: Python, Django, Django REST Framework
- ***База данных***: PostgreSQL
- ***Кэширование***: Redis
- ***Графовые алгоритмы***: NetworkX
- ***Frontend***: HTML, CSS, Bootstrap
- ***Инфраструктура***: Docker, Docker Compose, CI/CD через GitHub Actions
- ***Качество кода***: PEP8, pre-commit hooks (flake8, black, mypy), тесты

---

### <a id="title3"> 📂 Структура репозитория </a>
```bash
.
├── backend/          # Django проект и приложения
├── data/             # Исходные CSV из Kaggle
├── docs/             # Дополнительная документация
├── scripts/          # Скрипты для импорта и анализа данных
├── docker-compose.yml
├── README.md
└── requirements.txt
```

---

### <a id="title4"> 📊 API и функционал </a>

1. Добавление пользовательских взаимодействий
2. Получение рекомендаций (PageRank, CF, kNN)
3. Статистика и аналитика
4. Документация API (Swagger/ReDoc) будет доступна по адресу:
http://localhost:8000/api/docs/

---

### <a id="title5"> 🚀 Быстрый старт </a>
1. Клонировать репозиторий
    ```commandline
    git clone https://github.com/username/ecom-graph-recsys.git
    cd ecom-graph-recsys
    ```

2. Запустить проект
    ```commandline
    docker-compose up --build
    ```

---

### <a id="title6"> 📖 Документация </a>

Подробное описание алгоритмов, архитектуры и процесса запуска находится в папке `docs/`.

---

### <a id="title6"> 👨‍💻 Автор </a>

Разработано в рамках дипломного проекта.
 
**Автор**: Максим Лакович  
GitHub: [MaksimLakovich](https://github.com/MaksimLakovich)  
LinkedIn: [Maksim Lakovich](https://t.me/maksim_lakovich)  
Telegram: [@maksim_lakovich](https://t.me/maksim_lakovich)
