import requests
from bs4 import BeautifulSoup
import json


# Funkcja do pobierania danych autora z podstrony cytatu
def get_author_info(author_url):
    author_page = requests.get(author_url)
    author_soup = BeautifulSoup(author_page.content, 'html.parser')
    fullname = author_soup.find('h3').text.strip()
    born_date = author_soup.find(class_='author-born-date').text.strip()
    born_location = author_soup.find(class_='author-born-location').text.strip()
    description = author_soup.find(class_='author-description').text.strip()

    author_info = {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }
    return author_info


# Funkcja do pobierania cytatu z danej strony
def scrape_quotes(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    quotes = soup.find_all(class_='quote')

    all_quotes = []
    all_authors = []

    for quote in quotes:
        text = quote.find(class_='text').text.strip()
        author_name = quote.find(class_='author').text.strip()
        author_url = quote.find('a')['href']
        tags = [tag.text.strip() for tag in quote.find_all(class_='tag')]

        author_info = get_author_info('http://quotes.toscrape.com' + author_url)

        quote_info = {
            "tags": tags,
            "author": author_name,
            "quote": text
        }
        all_quotes.append(quote_info)
        all_authors.append(author_info)

    return all_quotes, all_authors


# Scrapowanie stron cytatu
all_quotes = []
all_authors = []
page_number = 1
while True:
    url = f'http://quotes.toscrape.com/page/{page_number}/'
    quotes, authors = scrape_quotes(url)
    if not quotes:
        break
    all_quotes.extend(quotes)
    all_authors.extend(authors)
    page_number += 1

# Zapis do pliku quotes.json
with open('quotes.json', 'w') as quotes_file:
    json.dump(all_quotes, quotes_file, indent=4)

# Zapis do pliku authors.json
with open('authors.json', 'w') as authors_file:
    json.dump(all_authors, authors_file, indent=4)