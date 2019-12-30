import calendar
import json,pymysql
import datetime
import pyssdb

conn={}
black_list = set()
cates = {'1': 'task', '2': 'user_manual', '4': 'chat', '8': 'query_answering'}

type1 = '10011 10014 10020 10023 10024 10025 10026 10028 10029 10030 10031 10037 10038 10039 10040 10041 10042 10043 10044 10045 10046 10047 10053 10063 10066 10067 10068 10069 10070 10071 10072 10073 10074'.split(
    ' ')
type1_with_intents = '10022 10032 10033 10034 10035 10036'.split(' ')
type1_intents = set(
    'phone_not_supported device_control_not_supported navi_not_supported robot_love_immediately robot_love_delay'.split(
        ' '))
type2_intents = set(
    'phone_not_supported device_control_not_supported navi_not_supported robot_love_immediately robot_love_delay'.split(
        ' '))
type3 = '10058 10018 10019 10021'.split(" ")

env='ds-mars-prod'

def init():
    #conn['ssdb'] = pyssdb.Client(host='10.86.11.20',port=31120)
    conn['ssdb'] = pyssdb.Client(host='10.25.9.37',port=13231)
    conn['db'] = pymysql.connect(
        host='10.25.9.37',
        port=3306,
        user='ndata',
        password='dsfEncr43slf',
        db='sariel',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )

    conn['db_ri'] = pymysql.connect(
        host='10.25.9.37',
        port=3306,
        user='ais-dev',
        password='QAdr45mfrkled',
        db='dialogue',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )

def get_yly():
    data = {}
    with conn['db_ops'].cursor() as c:
        c.execute("select id,text from recording_info")
        rs = c.fetchall()
        for r in rs:
            # YLY_000004
            data[r.get('text')] = "YLY_"+str(r.get('id')).zfill(6)
    return data

def get_yly_map():
    data = {}
    with conn['db_ops'].cursor() as c:
        c.execute("select id,text from recording_info")
        rs = c.fetchall()
        for r in rs:
            # YLY_000004
            data["YLY_"+str(r.get('id')).zfill(6)] = r.get('text')
    return data

def get_all_days():
    with conn['db'].cursor() as c:
        days = []
        c.execute('SELECT distinct(date(ts)) as dt FROM `prod_nomi_query`')
        rs = c.fetchall()
        for r in rs:
            dt = str(r.get('dt'))
            days.append(dt)
        return days

def get_week_key(monday):
    year = monday.isocalendar()[0]
    week = monday.isocalendar()[1]
    sunday = monday + datetime.timedelta(days=6)
    wstr = str(week).zfill(2)
    return f'w.{year}{wstr}'

def get_month_date_range(year,month):
    last_day = calendar.monthrange(year, month)[1]

    mstr = str(month).zfill(2)

    today = datetime.date.today()
    if today.year == year and today.month == month:
        last_day = today.day

    dr = (f'{year}-{mstr}-01', f'{year}-{mstr}-{last_day}')
    return dr

def get_month_day_num(year,month):
    last_day = calendar.monthrange(year, month)[1]
    today = datetime.date.today()
    if today.year == year and today.month == month:
        return today.day
    else:
        return last_day

def get_month_days(year,month):
    last_day = calendar.monthrange(year, month)[1]
    today = datetime.date.today()
    if today.year == year and today.month == month:
        return range(1,today.day+1)
    else:
        return range(1,last_day+1)

def get_month_key(year,month):
    mon = str(month).zfill(2)
    return f'm.{year}{mon}'

def get_set_from_ssdb(k):
    v = ssdb_get(k)
    if v == None:
        return None;
    return set(json.loads(v))

def ssdb_get(key):
    return conn['ssdb'].get(key)

def ssdb_get2(key):
    return conn['ssdb2'].get(key)

def ssdb_save(key,v):
    print(key)
    conn['ssdb'].set(key,v)

def ssdb_save_json(key,v):
    print(key)
    conn['ssdb'].set(key,json.dumps(v))

def date_count(c,sql,date_count):
    c.execute(sql,date_count)
    rs = c.fetchall()
    o = {}
    for r in rs:
        o[str(r.get('ts'))] = r.get('c')
    return o

def get_count(c,sql,pp):
    c.execute(sql, pp)
    return c.fetchone().get('c')

