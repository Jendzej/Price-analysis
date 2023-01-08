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


def analyze(json_data):
    """Analyze search results."""
    average_price = round(sum(list(map(get_price, json_data))) / len(list(map(get_price, json_data))), 2)
    rating = [x for x in list(map(get_rating, json_data)) if x is not None]
    opinions = [x[1] for x in rating]
    average_rating = round(sum(x[0] * x[1] for x in rating) / sum(opinions), 2)
    most_reviews = [x for x in json_data if 'opinions' in x.keys() and x['opinions'] == max(opinions)][0]

    lowest_price = [x for x in json_data if
                    x['price'] == min(y['price'] for y in json_data if type(y['price']) == float)]
    
    return {
        'average_price': average_price,
        'average_rating': average_rating,
        'opinions_count': sum(opinions),
        'most_popular_offer': most_reviews['url'],
        'cheapest_offer': min(y['price'] for y in json_data if type(y['price']) == float),
        'cheapest_offer_url': [x['url'] for x in lowest_price]
    }
