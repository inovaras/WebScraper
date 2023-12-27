FROM python:3.11
WORKDIR /web_scraper
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
WORKDIR /web_scraper
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0:8000"]
#CMD ["python", "manage.py", "async_parse_hub_and_fill_bd"]