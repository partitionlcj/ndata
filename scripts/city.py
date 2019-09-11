import json

def get_city(lat,lng):
    cities = json.load(open('city.json'))
    r = 9999999;
    city = ''
    for i in cities:
        [x1,y1] = cities[i]
        r1 = pow( (pow(lat - x1,2) + pow(lng - y1,2)), 0.5)
        if r1 < r:
            city = i
            r = r1
    return city

if __name__ == '__main__':
    #c = get_city(113.37438,23.12548)
    c = get_city(120.4951,31.45895)
    print(c)