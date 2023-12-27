FROM python:3.11
WORKDIR /web_scraper
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0:8000 && python manage.py async_parse_hub_and_fill_bd"]
