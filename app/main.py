import re

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from analyze import get_price, get_rating

driver = webdriver.Chrome()


def price_to_float(price: str):
    """Convert string price to float. For example: '329,99 zł' -> 329.99"""
    return float(''.join(re.findall('[0-9]*,?[0-9]*', price)).replace(',', '.'))


def currency_converter(currency_code: str, price: float):
    if currency_code == 'PLN':
        return price
    pln = requests.get(f'https://api.nbp.pl/api/exchangerates/rates/c/{currency_code}/?format=json')
    return round(price * pln.json()['rates'][0]['bid'], 2)


def assign_price(price, item: dict):
    if len(price) > 0:
        currency = 'PLN'
        if 'USD' in price[0]:
            currency = 'USD'
        elif '€' in price[0]:
            currency = 'EUR'
        if len(price) >= 2:
            item[
                'price'] = f'od {currency_converter(currency, price_to_float(price[0]))} do {currency_converter(currency, price_to_float(price[1]))}'
        else:
            item['price'] = currency_converter(currency, price_to_float(price[0]))


def rating_to_percentage(rating: str):
    """ Convert string rating to %. For example: 'Ocena: 4,5' -> 0.9 """
    converted = [x for x in re.findall('[0-9]*,?[0-9]*|[0-9]*,?[0-9]*/+[0-9]*', rating) if x]
    if len(converted) > 1:
        return round(float(converted[0].replace(',', '.')) / float(converted[1].replace('/', '')), 3)
    else:
        float_rating = float(converted[0].replace(',', '.'))
        if float_rating <= 5.0:
            return round(float_rating / 5, 3)
        elif float_rating <= 10.0:
            return round(float_rating / 10, 3)


def opinions_to_int(opinions: str):
    """Convert string opinions count to int. For example: '71 opinni' -> 71"""
    converted = [x for x in re.findall('[0-9]*', opinions.replace(' ', '')) if x]
    return int(converted[0])


def assign_values(response):
    assigned = []
    for element in response:
        if re.match('[0-9]*,?[0-9]*', element.text):
            item = {
                'url': element.find_element(By.XPATH, '..')
                .find_element(By.XPATH, '..')
                .find_element(By.TAG_NAME, 'a')
                .get_attribute('href')
            }
            price = re.findall(
                '[0-9] ?[0-9]*,?[0-9]* zł|[0-9] ?[0-9]*,?[0-9]* €|[0-9] ?[0-9]*,?[0-9]* USD',
                element.text)
            assign_price(price, item)

            rating = re.findall('Ocena: [0-9]*,?[0-9]*/*[0-9]*', element.text)

            opinions = re.findall('[0-9]* ?[0-9]+ ?op....|[0-9]* ?[0-9]* ?gł....', element.text)

            if 'price' in item.keys():
                if len(rating) != 0:
                    item['rating'] = rating_to_percentage(rating[0])
                if len(opinions) != 0:
                    item['opinions'] = opinions_to_int(opinions[0])

                assigned.append(item)
    return assigned


def analyze(json_data):
    """Analyze data search results."""
    average_price = round(sum(list(map(get_price, json_data))) / len(list(map(get_price, json_data))), 2)
    rating = [x for x in list(map(get_rating, json_data)) if x is not None]
    opinions = sum(x[1] for x in rating)
    average_rating = round(sum(x[0] * x[1] for x in rating) / opinions, 2)
    print("AVERAGE PRICE:", average_price)
    print("AVERAGE RATINGS:", average_rating)
    print("OPINIONS:", opinions)


def find_data(item_name):
    driver.get(f"https://www.google.com/search?q={item_name.replace(' ', '+')}")
    button = driver.find_element(By.XPATH, '//*[@id="W0wltc"]')
    button.click()
    WebDriverWait(driver, timeout=2).until(EC.presence_of_element_located((By.CLASS_NAME, 'fG8Fp')))
    data = driver.find_elements(By.CLASS_NAME, 'fG8Fp')
    json_data = assign_values(data)
    print(json_data)
    analyze(json_data)


if __name__ == "__main__":
    try:
        find_data('Soundcore life q30')
    except KeyboardInterrupt:
        driver.close()
