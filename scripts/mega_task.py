from config import *
from datetime import datetime, timedelta, date
from operator import truediv
import json, time

def zdiv(a,b):
  if b == 0:
    return 0
  else:
    return round(float(a/b),2)

def get_domains(c):
  c.execute('SELECT distinct(domain) as d FROM `debug_query`')
  rs = c.fetchall()
  domains = [r.get('d') for r in rs if r.get('d') != '']
  return domains

def gen_domain(c, d, env, appId, today):
  queries = date_count(c,f"SELECT hour(ts) as ts,count(1) as c FROM `debug_query` where env='{env}' and app_id='{appId}' and date(ts)=%s and domain=%s and length(query) > 0 group by hour(ts)",(today.strftime('%Y-%m-%d'),d))
  hour_query=[0]*24
  for i in queries.keys():
    hour_query[int(i)] = queries[i]
  return hour_query

def gen_daily_data(c, c2, dt, today, env, appId):
  tomorrow = today + timedelta(days=1)
  start = time.mktime(today.timetuple())*1000
  end = time.mktime(tomorrow.timetuple())*1000
  
  queryCount = get_count(c,f"select count(*) as c from debug_query where env='{env}' and app_id='{appId}' and date(ts)=%s and length(query) > 0",dt)
  vidCount = get_count(c,f"select count(distinct(vehicle_id)) as c FROM `debug_query` where env='{env}' and app_id='{appId}' and date(ts)=%s",dt)
  asrCount = get_count(c2,f"SELECT count(1) as c FROM `asr_request_info` where env='{env}' and app_id='{appId}' and `timestamp`> %s and `timestamp`< %s",[start,end]) 
  wakeup0Count = get_count(c2,f"SELECT count(1) as c FROM `wakeup_info` where env='{env}' and app_id='{appId}' and type = 0 and `timestamp`> %s and `timestamp`< %s",[start,end]) 
  wakeup4Count = get_count(c2,f"SELECT count(1) as c FROM `wakeup_info` where env='{env}' and app_id='{appId}' and type = 4 and `timestamp`> %s and `timestamp`< %s",[start,end]) 

  domain = {'head':[{
            "title": "domain",
            "key": "name"
          },
          {
            "title": "value",
            "key": "value"
          }
        ], "data": [
          {
            "name": "media",
            "value": 5214260
          }]}
  
  domain['data'] = date_count_nv(c,f"SELECT domain as ts,count(1) as c from debug_query where env='{env}' and app_id='{appId}' and date(ts)=%s and length(query) > 0 group by domain order by c desc ",dt)
  
  intent = {
        "head": [
          {
            "title": "intent",
            "key": "name"
          },
          {
            "title": "value",
            "key": "value"
          }
        ]}
  
  intent['data'] = date_count_nv(c,f"SELECT intents as ts,count(1) as c from debug_query where env='{env}' and app_id='{appId}' and date(ts)=%s group by intents order by c desc limit 10",dt)

  activeUser = {
        "head": [
          {
            "title": "vid",
            "key": "name"
          },
          {
            "title": "提车时间",
            "key": "attr"
          },
          {
            "title": "value",
            "key": "value"
          }
        ]}
  
  activeUser['data'] = date_count_nv(c,f"SELECT vehicle_id as ts,count(1) as c from debug_query where env='{env}' and app_id='{appId}' and date(ts)=%s group by vehicle_id order by c desc limit 20",dt)
  for i in activeUser['data']:
    i['attr'] = get_count(c,f"select DATE_FORMAT(activate_time,'%%Y%%m') as c from car_delivery where vehicle_id=%s",i['name'])

  MonthActiveUser = {
        "head": [
          {
            "title": "vid",
            "key": "name"
          },
          {
            "title": "提车时间",
            "key": "attr"
          },
          {
            "title": "value",
            "key": "value"
          }
        ]}
  
  MonthActiveUser['data'] = date_count_nv(c,f"SELECT vehicle_id as ts,count(1) as c from debug_query where env='{env}' and date_format(ts,'%%Y%%m')=%s group by vehicle_id order by c desc limit 20",dt[:7].replace('-',''))
  for i in MonthActiveUser['data']:
    i['attr'] = get_count(c,f"select DATE_FORMAT(activate_time,'%%Y%%m') as c from car_delivery where vehicle_id=%s",i['name'])

  r = {'queryCount':queryCount, 'vidCount':vidCount, 'asrCount': asrCount, 'activeUser':activeUser, 'wakeup0Count':wakeup0Count, 'wakeup4Count':wakeup4Count}
  ssdb_save_json(f"{env}.{appId}.total.info.use_nomi.d.{today.strftime('%Y%m%d')}", r)

def gen_hourly_data(c, c2, today, env , appId):
  tomorrow = today + timedelta(days=1)
  start = time.mktime(today.timetuple())*1000
  end = time.mktime(tomorrow.timetuple())*1000

  queries = date_count(c,f"SELECT hour(ts) as ts,count(1) as c FROM `debug_query` where env='{env}' and app_id='{appId}' and date(ts)=%s and length(query) > 0  group by hour(ts)",today.strftime('%Y-%m-%d'))
  hour_query=[0]*24
  for i in queries.keys():
    hour_query[int(i)] = queries[i]

  vids = date_count(c,f"SELECT hour(ts) as ts,count(distinct(vehicle_id)) as c FROM `debug_query` where env='{env}' and app_id='{appId}' and date(ts)=%s group by hour(ts)",today.strftime('%Y-%m-%d')) 
  hour_vid = [0]*24
  for i in vids.keys():
    hour_vid[int(i)] = vids[i]

#   vids = date_count(c2,f"SELECT hour(FROM_UNIXTIME(`timestamp`/1000)) as ts,count(distinct(vehicle_id)) as c FROM `asr_request_info` where env='{env}' and app_id='{appId}' and `timestamp`> %s and `timestamp`< %s group by hour(FROM_UNIXTIME(`timestamp`/1000))",[start,end])
#   hour_vid = [0]*24
#   for i in vids.keys():
#     hour_vid[int(i)] = vids[i]

  wakeups = date_count(c2,f"SELECT hour(FROM_UNIXTIME(`timestamp`/1000)) as ts,count(1) as c FROM `wakeup_info` where env='{env}' and app_id='{appId}' and (type=0 or type=4) and `timestamp`> %s and `timestamp`< %s group by hour(FROM_UNIXTIME(`timestamp`/1000))",[start,end]) 
  hour_wakeup = [0]*24
  for i in wakeups.keys():
    hour_wakeup[int(i)] = wakeups[i]

  asrs = date_count(c2,f"SELECT hour(FROM_UNIXTIME(`timestamp`/1000)) as ts,count(1) as c FROM `asr_request_info` where env='{env}' and app_id='{appId}' and `timestamp`> %s and `timestamp`< %s group by hour(FROM_UNIXTIME(`timestamp`/1000))",[start,end]) 
  hour_asr = [0]*24
  for i in asrs.keys():
    hour_asr[int(i)] = asrs[i]

  domains = get_domains(c)
  domainMap = {}
  for d in domains:
    domainMap[d.lower()] = gen_domain(c,d,env,appId,today)

  r = {'resultMap':{'queryCount':hour_query, 'wakeupCount':hour_wakeup,"vidCount":hour_vid, 'asrCount':hour_asr},'domainMap':domainMap}
  print(json.dumps(r))
  ssdb_save_json(f"{env}.{appId}.total.info.use_nomi_hours.d.{today.strftime('%Y%m%d')}", r)

def run_task(delta):
  init()
  db1 = conn['db']
  db2 = conn['db_ri']

  with db1.cursor() as c1, db2.cursor() as c2:
    today = date.today()
    today = today -  timedelta(days=delta)
    dt = today.strftime('%Y-%m-%d')
    
    gen_daily_data(c1,c2, dt,today,'ds-mars-prod', '100240130')
    gen_daily_data(c1,c2, dt,today,'ds-mars-prod', '100990130')
    gen_daily_data(c1,c2, dt,today,'ds-gn-prod', '100240001')

    # 杰克豆生产环境
    gen_hourly_data(c1,c2,today,'ds-mars-prod', '100240130')
    # 齐悟生产环境
    gen_hourly_data(c1,c2,today,'ds-mars-prod', '100990130')
    # 广蔚生产环境
    gen_hourly_data(c1,c2,today,'ds-gn-prod', '100240001')

if __name__ == '__main__':
    run_task(0)
