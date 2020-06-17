import pymysql
import json
from city import *
db = pymysql.connect(
        host='10.25.9.37',
        port=3306,
        user='ais-dev',
        password='QAdr45mfrkled',
        db='dialogue',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )

with db.cursor() as c:
    c.execute("select request_id from sariel.vos_debug_query where province = '' or province is null")
    rs = c.fetchall()
    i = 0
    for r in rs:
        rid = r.get('request_id')
 
        c.execute("select server_state from request_info where id=%s",rid)
        r1 = c.fetchone()
        if r1 == None:
            continue
        ss = json.loads(r1.get('server_state'))

        l = ss.get('location', None)
        city = ss.get('curCity', '')
        province = ss.get('province', '')

        if l:
            if 'curCity' in l :
                city = l.get('curCity', '')
                province = l.get('province', '')
            else:
                ll = l.split(",")
                ct = get_city(float(ll[0]),float(ll[1]))
                if city != '' and city != ct.get('name'):
                    print(f"{city} != {ct}, l={l}")
                city = ct.get('name')
                province = ct.get('province')
        print(f"{rid} {province}")
        c.execute('update sariel.vos_debug_query set city=%s, province=%s where request_id=%s',(city,province,rid))
        i = i + 1
        if i % 1000 == 0:
            db.commit()
        #c.execute('select * from cnarea_2016 where id=%s',pid)
    db.commit()
