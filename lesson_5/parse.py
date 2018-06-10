from bs4 import BeautifulSoup
from req import get_html

html = get_html('https://yandex.ru/search/?lr=213&msid='\
                '1528612135.02252.22874.1830&text=python')

if html:
    bs = BeautifulSoup(html, 'html.parser')

    data = []

    for item in bs.find_all('li', class_='serp-item'):
        block_title = item.find('a', class_='organic__url')
        href = item.find('a', class_='path__item')
        data.append({
            'title': block_title.text,
            'link': href.get('href')
            })

    print(data)
else:
    print("OMG. I've broke the internet!")    

