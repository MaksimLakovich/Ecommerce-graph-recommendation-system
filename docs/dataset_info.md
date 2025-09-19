## Описание, как скачивать оригинальный dataset с Kaggle и как создавать собственные сэмплы, если нужно уменьшить или увеличить объем в них

---

### 1. Установка оригинального датасета в 'data/' (шаги для macOS и Windows)
- Шаг 1: Получить API-токен Kaggle.  
  Зарегистрируйтесь / войдите в аккаунт Kaggle: https://www.kaggle.com


- Шаг 2: Перейдите в Account / API и нажмите Create New API Token.  
  В результате скачается файл `kaggle.json`.


- Шаг 3: Разместить `kaggle.json`.
  - **для macOS**:  
    - Проверь, где лежит скачанный kaggle.json. Обычно — в ~/Downloads:
      ```commandline
      ls -l ~/Downloads | grep kaggle.json
      ```
    - Создай папку ~/.kaggle (если её нет) и перемести туда файл:
      ```commandline
      mkdir -p ~/.kaggle
      mv ~/Downloads/kaggle.json ~/.kaggle/
      ```
      Если kaggle.json оказался в другой папке, то замени ~/Downloads/kaggle.json на реальный путь.
    - Установи права доступа (ОЧЕНЬ важно - kaggle требует 600). Это делает файл доступным только тебе что безопасно:
      ```commandline
      chmod 600 ~/.kaggle/kaggle.json
      ```
    - Убедись, что файл на месте. Сat выведет JSON с двумя полями username и key:
      ```commandline
      ls -l ~/.kaggle
      cat ~/.kaggle/kaggle.json
      ```
  - **для Windows PowerShell**:
    ```powershell
    $kaggle="$env:USERPROFILE\.kaggle"
    New-Item -ItemType Directory -Force -Path $kaggle
    Move-Item -Path "$env:USERPROFILE\Downloads\kaggle.json" -Destination "$kaggle\kaggle.json"
    ```


- Шаг 4: Установка kaggle CLI.  
  С помощью окружения проекта через poetry:
  ```commandline
  poetry add --dev kaggle
  ```


- Шаг 5: Проверка доступа (poetry).  
  Показать файлы датасета (проверка, что ключ настроен правильно)  
  ```commandline
  poetry run kaggle datasets files -d psparks/instacart-market-basket-analysis
  ```


- Шаг 6: Скачивание и распаковка.
  - **для macOS**:  
    ```commandline
    mkdir -p data
    poetry run kaggle datasets download -d psparks/instacart-market-basket-analysis -p data --unzip
    # если --unzip не поддерживается:
    # poetry run kaggle datasets download -d psparks/instacart-market-basket-analysis -p data
    # unzip data/instacart-market-basket-analysis.zip -d data/
    ```
  - **для Windows PowerShell**:  
    ```commandline
    mkdir data
    poetry run kaggle datasets download -d psparks/instacart-market-basket-analysis -p data
    # распаковать
    Expand-Archive -Path data\instacart-market-basket-analysis.zip -DestinationPath data
    ```


- Шаг 7: Объединение order_products__prior.csv и order_products__train.csv.
  - **для macOS**:  
    ```commandline
    # создаём заголовок (берём его из первого файла), затем добавляем все строки из обоих файлов, пропуская второй заголовок
    (head -n 1 data/order_products__prior.csv && tail -n +2 -q data/order_products__prior.csv data/order_products__train.csv) > data/order_products_all.csv
    ```
  - **для Windows PowerShell**:  
    ```commandline
    # записать заголовок
    Get-Content data\order_products__prior.csv -TotalCount 1 | Out-File data\order_products_all.csv
    # добавить все строки, пропуская первую строку (заголовок)
    Get-Content data\order_products__prior.csv | Select-Object -Skip 1 | Out-File -Append data\order_products_all.csv
    Get-Content data\order_products__train.csv | Select-Object -Skip 1 | Out-File -Append data\order_products_all.csv
    ```


- Шаг 8: Добавьте data/ в .gitignore, чтобы не пушить полный датасет в репозиторий.  


- Шаг 9: Загружаем данные из CSV датасета в таблицы PostgreSQL.

---

### 2. Создание и использование samples с минимальными данными из 'sample_data/'

1. Если хотите быстро запустить приложение без загрузки полного набора данных, то вы можете использовать готовые samples в `sample_data/`


2. Если есть необходимость создать собственные сэмплы (более расширенные или, наоборот, еще более маленькие), то вы можете скачать оригинальный датасет (см. пункт 1 выше), а потом использовать функцию `sample_data/make_samples.py`.  
   - Функция `make_samples.py` позволяет:
     - задавать любое количество строк в выборке, например, 1% или 58% строк из CSV
     - задавать свою "случайность" в random_state=... 
   - Команда для запуска функции (после загрузки оригинального датасета):
     ```commandline
     poetry run python sample_data/make_samples.py
     ```
