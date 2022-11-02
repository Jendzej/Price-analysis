from array import array
from urllib.request import ProxyBasicAuthHandler
import requests
import dotenv
import os
from bs4 import BeautifulSoup
import re


def clearPrice(priceElement: array):
    prices = []
    for i, price in enumerate(priceElement): # range(len(priceElement)) is bad, enumerate(priceElement) is better as you get both the index and item
    # but even if you are not using the index, you can just do "for price in priceElement:"
        price = price.text.strip()
        priceClear = re.findall("[0-9]|,", price.strip())
        prices.append(float("".join(priceClear).replace(",",".")))
    return [priceElement, prices] # That kinda makes sense but why though? What's the point of keeping the dirty version of the price?


def avaragePrice(priceList: array):
    return round(sum(priceList) / len(priceList))


def main():
    dotenv.load_dotenv()
    url = os.getenv("URL")

    search = re.search(r"morele\.net\/wyszukiwarka\/", url) # That's one of the ways to make it idiotproof
    # Since no info is provided on the specs of the URL, we have to assume that user may include
    # - www.
    # - https://
    # - anything after the last slash
    # We can always add ^ and $ to the regex to make it more strict, and then notify the user on how the URL should look (but they are idiots though?)
    if search == None:
        print("Wrong URL")
        return

    item = input("Type item to search (morele.net): ")
    response = requests.get(f'{url}?q={item.replace(" ", "+")}')
    if response.status_code != 200:
        print("Something went wrong while getting the price from the website.")
        return
    prettyResponse = BeautifulSoup(response.content, 'html.parser')
    price = prettyResponse.find_all("div", {"class":"price-new"})
    print(f"Most accurate price for your ask ({item}) is: {price[0].text.strip()}")
    price = clearPrice(price)
    avgPrice = avaragePrice(price[1])
    print(f"Avarage price for your ask is: {avgPrice} zł")

if __name__ == "__main__":
    main()
