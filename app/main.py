import requests
import dotenv
import os
from bs4 import BeautifulSoup


def main():
    dotenv.load_dotenv()
    url = os.getenv("URL")
    item = os.getenv("ITEM")
    response = requests.get(f'{url}q={item.replace(" ", "+")}')
    prettyResponse = BeautifulSoup(response.content, 'html.parser')
    price = prettyResponse.find_all("div", {"class":"price-new"})
    print(f"Most accurate price for your ask ({item}) is: {price[0].text.strip()}")

if __name__ == "__main__":
    main()
