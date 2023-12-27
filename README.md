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

LVL5: Упаковать всё Docker-образ. 

## Как запустить проект:

Клонировать репозиторий:

```
git clone https://github.com/inovaras/WebScraper.git
```

Перейти в него в командной строке:
```
cd WebScraper
```

Выполнить команду:

```
docker compose up

```

Все готово!
Можно зайти в админку смотреть необходимую информацию по статьям с habr.com

Админка http://127.0.0.1:8000/admin/parser/article/
Заходить под суперпользователем:

```
username: admin
password: 1 
```

