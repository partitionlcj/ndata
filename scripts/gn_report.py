from navi_funnel import *
from call_funnel import *
import retention
from datetime import datetime, timedelta, date
from config_gn import *

env='ds-mars-prod'

def hot_domains(c,date_range,key):
    domain_count = date_count(c, f"select domain as ts,count(1) as c from debug_query where  date(ts)>=%s and date(ts)<=%s and catemr='task' group by domain order by c desc",date_range)
    ssdb_save_json(f'{env}.base.domain.' + key, domain_count)
    huashu_count = date_count(c,f"select catemr as ts,count(1) as c from debug_query where  date(ts)>=%s and date(ts)<=%s group by catemr order by c desc",date_range)
    ssdb_save_json(f'{env}.base.huashu.'+key,huashu_count)

def hot_intents(c,date_range,key):
    intent_count = date_count(c,f"select intents as ts,count(1) as c from debug_query where  date(ts)>=%s and date(ts)<=%s and catemr='task' group by intents order by c desc",date_range)
    ssdb_save_json(f'{env}.base.intents.' + key, intent_count)

def nlu_type(c,date_range,key):
    nt = date_count(c, f"select nlu_type as ts,count(*) as c from debug_query where  date(ts)>=%s and date(ts)<=%s group by nlu_type",date_range)
    #data = {'正常':nt['0'],"nlu正常走兜底":nt['1'],'nlu部分理解走兜底':nt['2'],'nlu完全不理解':nt['3']}
    data = {'0': nt.get('0',0), "1": nt.get('1',0), '2': nt.get('2',0), '3': nt.get('3',0)}
    ssdb_save_json(f'{env}.base.nlu_type.' + key, data)

def nlu_type_data(c,date_range,key):
    c.execute(f"select nlu_type,session_id from debug_query where  date(ts)>=%s and date(ts)<=%s",date_range)
    rs = c.fetchall()
    data = [[],[],[],[]]

    for r in rs:
        type = r.get('nlu_type')
        data[type].append(r.get('session_id'))
    for i in range(1,4):
        ssdb_save_json(f'{env}.base.nlu_type.' + key+"."+ str(i), data[i])

def hour_distrib(c, pp, key):
    hour_query = date_count(c,f"SELECT hour(ts) as ts,count(1) as c FROM `debug_query` where  date(ts)>=%s and date(ts)<=%s group by hour(ts)",pp)
    ssdb_save_json(f'{env}.base.hourly.' + key, hour_query)

def basic_usage(c, pp, key):
    # query数
    date_query = get_count(c,f"SELECT count(1) as c FROM `debug_query` where  date(ts)>=%s and date(ts)<=%s",pp)
    # session数
    date_session = get_count(c,f"SELECT count(distinct(session_id)) as c FROM `debug_query` where  date(ts)>=%s and date(ts)<=%s",pp)
    # 使用车辆数
    c.execute(f"select distinct(vehicle_id) as vid from debug_query where  date(ts)>=%s and date(ts)<=%s",pp)
    act_vids = []
    rs = c.fetchall()
    for r in rs:
        act_vids.append(r.get('vid'))
    ssdb_save_json(f"{env}.base.active_vids.{key}", act_vids)

    data = {'query': date_query, 'session': date_session, 'active_vid': len(act_vids)}

    ssdb_save_json(f"{env}.base.info." + key, data)

def total_domain_intents_dist(c):
    huashu_dist = date_count(c,f"select catemr as ts,count(1) as c from debug_query group by catemr",())
    domain_dist = date_count(c,f"select domain as ts,count(1) as c from debug_query where  catemr='task' group by domain",())
    intents_dist = date_count(c,f"select intents as ts,count(1) as c from debug_query where  catemr='task' group by domain",())

    ssdb_save_json(f"{env}.total.domain",domain_dist)
    ssdb_save_json(f"{env}.total.huashu",huashu_dist)
    ssdb_save_json(f"{env}.total.intents", intents_dist)

    c.execute(f"SELECT distinct(domain) as d FROM `debug_query`")
    rs = c.fetchall()
    for r in rs:
        d = r.get('d')
        intent_dist = date_count(c,f"select intents as ts,count(1) as c from debug_query where  catemr='task' and domain=%s group by intents",(d))
        ssdb_save_json(f'{env}.total.intents.'+d.lower(), intent_dist)

def snapshot_report(c,k):
    total_domain_intents_dist(c)

def city_query(c,dr, key):
    cq = date_count(c,f"select city as ts,count(request_id) as c from debug_query where  date(ts)>=%s and date(ts)<=%s group by city",dr)
    cv = date_count(c,f"select city as ts,count(distinct(vehicle_id)) as c from debug_query where  date(ts)>=%s and date(ts)<=%s group by city",dr)

    data = []
    for i in cv:
        l = {'city':i,'总query':cq[i],'到达车辆':cv[i]}
        data.append(l)

    ssdb_save_json(f"{env}.base.city.{key}", data)


def query_frequency(c,dr,key):
    c.execute(f"select query as q,count(1) as c from debug_query where env='ds-gn-prod' and date(ts)>=%s and date(ts)<=%s and length(query)>0 and query != 'N/A'  group by query order by c desc limit 200",dr)
    rs = c.fetchall()
    o = []
    for r in rs:
        o.append({'query':r.get('q'),'count':r.get('c')})

    ssdb_save_json(f"{env}.query.frequency.{key}",o)

def period_report(c, dr, k,detail_info=False):
    hot_domains(c, dr, k)
    hot_intents(c, dr, k)
    nlu_type(c, dr, k)
    nlu_type_data(c, dr, k)
    basic_usage(c, dr, k)
    hour_distrib(c, dr, k)
    query_frequency(c, dr, k)
    city_query(c,dr,k)

def nomi_usage_vids(c,dr,key):
    cq = date_count(c, f"select vehicle_id as ts,count(request_id) as c from debug_query where  date(ts)>=%s and date(ts)<=%s group by vehicle_id",dr)
    # vu = date_count(c, "select vehicle_id as ts ,DATEDIFF(%s,activate_time) as c from es8_delivery where  type=1 and date(activate_time)<=%s",(dr[1],dr[1]))
    # vd = date_count(c,"select vehicle_id as ts ,date(activate_time) as c from es8_delivery where type=1",())

    dt = datetime.strptime(dr[1], "%Y-%m-%d")
    # 当月最大天数
    day_num = get_month_day_num(dt.year,dt.month)

    data = []
    for i in vu:
        days_of_this_month = min(vu[i]+1,day_num)
        total_query = 0
        daily_query = 0
        if i in cq:
            total_query = cq[i]
            daily_query = "{:.1f}".format(float(cq[i])/(days_of_this_month))

        l = {'vid':i,'query总数':total_query,'本月日均query':daily_query,'本月末为止提车天数':vu[i]+1,'提车日期':str(vd[i])}
        data.append(l)
    ssdb_save_json('vid.usage.'+key,data)

def daily_report(c,dt):
    c.execute("SET time_zone = '+8:00'")
    k = 'd.'+dt.replace("-","")
    dr = (dt,dt)

    period_report(c,dr,k,detail_info=True)
    #retention.daily(datetime.strptime(dt, "%Y-%m-%d"))

def weekly_report(c,monday):
    c.execute("SET time_zone = '+8:00'")
    year = monday.isocalendar()[0]
    week = monday.isocalendar()[1]
    sunday = monday + timedelta(days=6)
    wstr = str(week).zfill(2)
    k = f'w.{year}{wstr}'

    dr = ( monday.strftime('%Y-%m-%d'), sunday.strftime('%Y-%m-%d'))
    period_report(c,dr,k, detail_info=False)
    #retention.weekly(monday)

def monthly_report(c, year,month):
    c.execute("SET time_zone = '+8:00'")
    dr = get_month_date_range(year,month)
    m_key = get_month_key(year,month)

    period_report(c,dr,m_key, detail_info=False)
    #nomi_usage_vids(c,dr,m_key)

    #retention.monthly(year,month)

def gen_all_daily_data(c):
    for dt in get_all_days():
        daily_report(c,dt)

def gen_all_monthly_data(c):
    for i in range(6,11):
        monthly_report(c,2018, i)

def gen_all_weekly_data(c):
    dt = datetime.now()
    for i in range(0,12):
        monday = dt - timedelta(days=(dt.weekday() + i*7))
        weekly_report(c,monday)

def gen_all_report(c):
    gen_all_weekly_data(c)
    gen_all_monthly_data(c)
    gen_all_daily_data(c)

def today(c):
    today = date.today()
    daily_report(c, today.strftime('%Y-%m-%d'))
    for i in range(0,5):
        yesterday = today - timedelta(days=i)
        daily_report(c, yesterday.strftime('%Y-%m-%d'))
    for i in range(0,3):
        monday = today - timedelta(days=(today.weekday() + i*7))
        weekly_report(c,monday)
    monthly_report(c, 2020, today.month)
    monthly_report(c, 2020, today.month-1)
    monthly_report(c, 2020, today.month-2)

    snapshot_report(c, 'd.' + yesterday.strftime('%Y%m%d'))

def prod(c):
    today(c)

def dev(c):
    gen_all_report(c)
    # total_domain_intents_dist(c)
    # monthly_report(c, 2018, 10)
    # gen_all_monthly_data(c)
    # gen_all_daily_data(c)


if __name__ == '__main__':
    init()
    db = conn['db']

    with db.cursor() as c:
        prod(c)
        today = date.today()
        yesterday = today - timedelta(days=1)
        daily_report(c, yesterday.strftime('%Y-%m-%d'))