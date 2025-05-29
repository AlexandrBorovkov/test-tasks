import requests
import csv

from bs4 import BeautifulSoup
from collections import Counter
from urllib.parse import urljoin, unquote


RUSSIAN_ORDER = [
    'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Ё', 'Ж', 'З', 'И', 'Й',
    'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф',
    'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Э', 'Ю', 'Я'
]

def parsing_wikipedia():
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    domain = "https://ru.wikipedia.org"
    current_url = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
    page_num = 1
    result_list = []
    while current_url:
        print(f"Парсинг страницы {page_num}")
        try:
            response = requests.get(current_url, headers=headers)
            response.encoding = "utf-8"
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            for link in soup.select('div.mw-category-group > ul > li > a'):
                name = link.text
                if name[0] in RUSSIAN_ORDER:
                    result_list.append(name[0])
            next_link = soup.select_one('div#mw-pages a:-soup-contains("Следующая страница")')
            if next_link:
                decoded_link = unquote(next_link['href'])
                current_url = urljoin(domain, decoded_link)
                if current_url == ("https://ru.wikipedia.org/w/index.php?"
                                   "title=Категория:Животные_по_алфавиту&"
                                   "pagefrom=Японский+бурый+медведь#mw-pages"):
                    print("Последняя страница")
                    return result_list
                page_num += 1
            else:
                print("Последняя страница")
                return result_list
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при загрузке страницы: {e}")
            return

def record_data(data):
    sorted_data = [(key, data[key]) for key in RUSSIAN_ORDER if key in data]
    with open("beasts.csv", "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in sorted_data:
            writer.writerow(row)


if __name__ == '__main__':
    data = Counter(parsing_wikipedia())
    record_data(data)
