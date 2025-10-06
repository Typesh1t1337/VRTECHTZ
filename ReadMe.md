# Тестовое задание: Парсер Kaspi магазина  

## 📌 Описание проекта  

Программа парсит html страницу kaspi товаров и собирает информацию через js-бандлы,
так же парсит api который я реверснул на странице.
Парсит данные как:
- название
- описание
- мин цена
- макс цена
- категорию
- рейтинг
- количество отзывов
- количество продавцов
- и список фото
- История цен в отдельной таблице
- История офферов в отдельной таблице

Данные сохраняются в POSTGRESQL, JSON в папку export,которая генерируется
Так же использовал селери, чтобы каждые 15 минут парсить каспи и пересохранять данные,
так же историю

доп возможности:
отображение истории, так же отображение всех сохраненных записей в бд


## 🚀 Установка и запуск  

### 1. Клонирование репозитория  

git clone git@github.com:Typesh1t1337/VRTECHTZ.git

### 2. Установка зависимостей  
pip install -r requirements.txt  

### 3. Настройка окружения  
Создайте файл `.env` и укажите:  
POSTGRES_PASSWORD=ZHALGASIKSUPERLOX2007
POSTGRES_USER=ZHALGO
POSTGRES_DB=test_postgres
POSTGRES_PORT=5432
POSTGRES_HOST=db
CELERY_BROKER=redis://redis:6379/0
CELERY_RESULT=redis://redis:6379/1

### 4. установка контейнера докер
docker-compose up --build

## 🗄️ PostgreSQL

products

id — PK, уникальный идентификатор продукта
name — название продукта
kaspi_id — уникальный ID продукта на Kaspi
description — описание продукта
category — категория продукта
min_price — минимальная цена
max_price — максимальная цена
rate — рейтинг продукта
review_amount — количество отзывов
seller_amount — количество продавцов
image_url — массив ссылок на изображения

product_history

id — PK, уникальный идентификатор записи истории
product_id — FK на products.id
name — название продукта на момент проверки
description — описание продукта на момент проверки
category — категория на момент проверки
min_price — минимальная цена на момент проверки
max_price — максимальная цена на момент проверки
rate — рейтинг на момент проверки
review_amount — количество отзывов на момент проверки
seller_amount — количество продавцов на момент проверки
checked_at — дата и время проверки
image_url — массив ссылок на изображения

offers

id — PK, уникальный идентификатор оффера
product_id — FK на products.id
seller — название продавца
price — цена оффера

offer_history

id — PK, уникальный идентификатор записи истории
product_id — FK на products.id
offer_id — FK на offers.id
seller — название продавца
price — цена оффера на момент проверки
created_at — дата и время создания записи истории


## 🔄 Обновления данных  
- Интервал: 15 минут  
- Обновляются поля как: "description", "category", "min_price", "max_price", "rate", "review_amount",
                          "seller_amount"

## 📝 Пример логов  
{"asctime": "2025-10-06 10:17:35,081", "levelname": "INFO", "module": "base", "message": "select current_schema()"}
{"asctime": "2025-10-06 10:17:35,081", "levelname": "INFO", "module": "base", "message": "[raw sql] ()"}
{"asctime": "2025-10-06 11:01:24,836", "levelname": "INFO", "message": "Celery task 'update_products' started"}
{"asctime": "2025-10-06 11:01:25,211", "levelname": "INFO", "message": "", "type": "task_finished", "product_id": 14}
{"asctime": "2025-10-06 11:17:48,422", "levelname": "INFO", "message": "Celery task 'update_products' started"}


## ✅ Что сделано  
- [x] Парсинг товара   
- [x] Сохранение в PostgreSQL  
- [x] Экспорт в JSON  
- [x] Логирование  
- [x] Docker  
- [x] Alembic миграции  
- [x] Расширенный сбор за исключением характеристик
- [x] Логирование в JSON
- [x] Экспорт offers
