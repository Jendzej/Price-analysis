import re


def get_price(item: dict):
    if type(item['price']) == float:
        return item['price']
    else:
        prices = [float(x) for x in re.findall('[0-9]*[.]?[0-9*]*', item['price']) if x]
        return round(sum(prices) / len(prices), 2)


def get_rating(item: dict):
    if 'rating' in item.keys() and 'opinions' in item.keys():
        return item['rating'], item['opinions']
