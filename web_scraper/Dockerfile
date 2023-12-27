FROM python:3.11
WORKDIR /web_scraper
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]