from bs4 import BeautifulSoup as BS
import requests
import re

basic_url = "https://sbermegamarket.ru/catalog/?q="


def findProduct(product_name):
    url = basic_url + product_name
    page = requests.get(url)
    page.encoding = 'utf8'

    soup = BS(page.text, "html.parser")

    all_products = soup.findAll(class_='inner')

    filtered_names = []
    filtered_prices = []
    filtered_ref = []

    for data in all_products:
        if data.find(class_='item-title') is not None:
            filtered_names.append(data.text)
        if data.find('meta') is not None:
            s = str(data.text)
            s = re.sub('\d{1,}%', '', s)
            match = re.search(r'(\d{1,} {0,}){1,}', s)
            if match:
                filtered_prices.append(re.sub(' ', '', match[0]))
        for ref in data.find_all('a', class_='ddl_product_link', href=True):
            s = str(ref["href"])
            s = re.sub('#.*', '', s)
            filtered_ref.append('https://sbermegamarket.ru' + s)

    d = {}
    d["cost"] = None
    d["product name"] = None
    d["link"] = None

    if len(filtered_names):
        d['product name'] = filtered_names[0]
    if len(filtered_prices):
        d['cost'] = int(filtered_prices[0])
    if len(filtered_ref):
        d['link'] = filtered_ref[0]
    return d
