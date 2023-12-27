# WebScraper
Парсер с habr.com:

1) Парсер раз в 10 минут делает запрос на главную страницу хаба.
2) Берет с главной страницы хаба ссылки на статьи.
3) Для каждой собранной ссылки посещает страницу статьи и собрает информацию о статье (заголовок, дата, ссылка на пост, имя автор, ссылка на автора).
4) Выводит информацию на консоль

А также:

LVL1: Сохраняет данные в базу данных sqlite3 с текстом публикации. 

LVL2: Создает таблицу в базе данных с информацией о хабах.
      Добавляет в созданную таблицу все хабы.

LVL3: Парсер асинхронный, используется библиотека aiohttp

LVL4: Добавлена админка на Django для отображения хабов и управления ими (можно добавить хаб/удалить хаб).

## Как запустить проект:

Клонировать репозиторий:

```
git clone https://github.com/inovaras/WebScraper.git
```

Перейти в него в командной строке:
```
cd WebScraper
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv 
(Для Linux: python3 -m venv venv)
```

```
source venv/Scripts/activate  
(Для Linux: source venv/bin/activate)
```

```
python -m pip install --upgrade pip 
(Для Linux: python3 -m pip install --upgrade pip)
```

Установить зависимости из файла requirements.txt:

```
cd web_scraper
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py makemigrations
python manage.py migrate

(Для Linux: 
python3 manage.py makemigrations
python3 manage.py migrate
)
```


Проект запускается в 2 этапа:
1) Запуск Админки
2) Запуск скрипта парсера https://habr.com/ru и загрузки данных в бд находится в 

## Этап 1:
```
python manage.py runserver
(Для Linux: python3 manage.py runserver)

```
Админка http://127.0.0.1:8000/admin/parser/article/

Для админки:

Создать суперпользователя
```
python manage.py createsuperuser
(Для Linux: python3 manage.py createsuperuser)
```
если использовать готовую БД, то есть пользователь:
```
username: admin
password: 1 
```
## Этап 2:

## Запуск скрипта по команде:
Параллельно в другом терминале перейти в директорию web_scraper:
```
cd web_scraper
```
Запустить скрипт для парсинги и заполнения БД по команде:
```
python manage.py async_parse_hub_and_fill_bd
(Для Linux: python3 manage.py async_parse_hub_and_fill_bd)
```

## Дополнительные сведения:
1) Скрипт парсера https://habr.com/ru и загрузки данных в бд находится в

```web_scraper > parser > management > commands > async_parse_hub_and_fill_bd``` 

2)  Собранную БД можно посмотреть ```web_scraper > parser > db.sqlite3``` таблица ```parser_article```
