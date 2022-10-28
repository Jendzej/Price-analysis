from array import array
from urllib.request import ProxyBasicAuthHandler
import requests
import dotenv
import os
from bs4 import BeautifulSoup
import re


def clearPrice(priceElement: array):
    prices = []
    for i in range(len(priceElement)):
        priceElement[i] = priceElement[i].text.strip()
        priceClear = re.findall("[0-9]|,", priceElement[i].strip())
        prices.append(float("".join(priceClear).replace(",",".")))
    return [priceElement, prices]


def avaragePrice(priceList: array):
    return round(sum(priceList) / len(priceList))


def main():
    dotenv.load_dotenv()
    url = os.getenv("URL")
    # item = os.getenv("ITEM")
    item = input("Type item to search (morele.net): ")
    response = requests.get(f'{url}q={item.replace(" ", "+")}')
    prettyResponse = BeautifulSoup(response.content, 'html.parser')
    price = prettyResponse.find_all("div", {"class":"price-new"})
    print(f"Most accurate price for your ask ({item}) is: {price[0].text.strip()}")
    price = clearPrice(price)
    avgPrice = avaragePrice(price[1])
    print(f"Avarage price for your ask is: {avgPrice} zł")

if __name__ == "__main__":
    main()
