import json

cities = json.load(open('city.json'))

def get_city(lng,lat):
    r = 99999999;
    city = None
    for c in cities:
        x1 = float(c.get('lat'))
        y1 = float(c.get('lng'))
        r1 = pow( (pow(lat - x1,2) + pow(lng - y1,2)), 0.5)
        if r1 < r:
            city = c
            r = r1
    return city

if __name__ == '__main__':
    #c = get_city(113.37438,23.12548)
    c = get_city(116.4951,39.90895)
    print(c)
