import pymysql
import json

db = pymysql.connect(
        host='10.25.9.37',
        port=3306,
        user='ais-dev',
        password='QAdr45mfrkled',
        db='crawler',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )

with db.cursor() as c:
    c.execute("select * from cnarea_2016 where level=1")
    rs = c.fetchall()
    cities = []
    for r in rs:
        pid = r.get('parent_id')
        c.execute('select * from cnarea_2016 where id=%s',pid)
        r1 = c.fetchone()
        province = r1.get("name")
        city = { 'name' : r.get('name'), 'province':province,'lng' : str(r.get('lng')), 'lat' : str(r.get('lat')) }
        cities.append(city)
    json.dump(cities, open('city.json','w'), ensure_ascii=False)
