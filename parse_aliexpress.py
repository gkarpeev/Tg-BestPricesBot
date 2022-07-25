from bs4 import BeautifulSoup as BS
import requests
import re

basic_url = "https://aliexpress.ru/wholesale?catId=&SearchText="


def findProduct(product_name):
    url = basic_url + product_name
    page = requests.get(url)
    page.encoding = 'utf8'

    soup = BS(page.text, "html.parser")

    all_products = soup.findAll(
                    class_='product-snippet_ProductSnippet__content__1yqrun')

    filtered_names = []
    filtered_prices = []
    filtered_ref = []

    for data in all_products:
        res = data.find(class_='product-snippet_ProductSnippet__name__1yqrun')
        if res is not None:
            filtered_names.append(res.text)
        res = data.find(class_='snow-price_SnowPrice__mainM__2y0jkd')
        if res is not None:
            filtered_prices.append(
                re.sub('[^\d]', '', re.sub(',.*', '', res.text)))
        for ref in data.find_all('a', href=True):
            s = str(ref["href"])
            filtered_ref.append('https://aliexpress.ru' + s)
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
