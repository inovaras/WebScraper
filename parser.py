import requests
import json
from bs4 import BeautifulSoup as bs
import time


def get_main_page():
    url = 'https://habr.com/ru/'
    response = requests.get(url)
    with open("main.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
    return response.text


def parse_main_page(html):
    soup = bs(html, 'html.parser')
    hub_links = soup.find_all('a', class_="tm-title__link")
    with open("main_info.txt", "w", encoding="utf-8") as file:
        for link in hub_links:
            file.write(f"hub_link: {link}\n")

    article_links = ["https://habr.com"+link['href'] for link in hub_links]
    with open("article_links.txt", "a", encoding="utf-8") as file:
        for link in article_links:
            file.write(f"hub_link: {link}\n")
    return article_links


def parse_article_page(article_url):
    response = requests.get(article_url)
    with open("article.txt", "w", encoding="utf-8") as file:
        file.write(response.text)
    print(response.status_code)
    soup = bs(response.text, 'html.parser')
    script_content = soup.find('script', {'data-vue-meta': 'ssr', 'type': 'application/ld+json'}).string
    author_content = soup.find('a', class_='tm-user-info__username')
    data = json.loads(script_content)
    title = data.get('headline', '')
    date = data.get('datePublished', '')
    author_name = data.get('author', '').get('name')
    author_url = 'https://habr.com'+author_content['href']

    return {
        'title': title,
        'date': date,
        'article_url': article_url,
        'author_name': author_name,
        'author_url': author_url
    }


def main():
    while True:
        print("Получаю данные с Хабра...")
        main_page_html = get_main_page()
        article_links = parse_main_page(main_page_html)

        for article_link in article_links:
            article_info = parse_article_page(article_link)
            print("\nArticle Information:")
            print(f"Title: {article_info['title']}")
            print(f"Date: {article_info['date']}")
            print(f"URL: {article_info['article_url']}")
            print(f"Author: {article_info['author_name']}")
            print(f"Author URL: {article_info['author_url']}")
            print("-" * 50)

        print("Жду 10 минут...")
        time.sleep(600)  # Wait for 10 minutes


if __name__ == '__main__':
    main()
