from config import *
from datetime import datetime, timedelta, date
from operator import truediv
import json

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

def gen_domain(c, d, today):
  queries = date_count(c,f"SELECT hour(ts) as ts,count(1) as c FROM `debug_query` where env='{env}' and date(ts)=%s and domain=%s group by hour(ts)",(today.strftime('%Y-%m-%d'),d))
  hour_query=[0]*24
  for i in queries.keys():
    hour_query[int(i)] = queries[i]
  return hour_query

def gen_daily_data(c,dt,today):
  queryCount = get_count(c,f"select count(*) as c from debug_query where env='{env}' and date(ts)=%s",dt)
  sessionCount = get_count(c,f"select count(distinct(session_id)) as c from debug_query where env='{env}' and date(ts)=%s",dt)
  onlineSessionCount = sessionCount
  offlineSessionCount = 0
  cityCount = get_count(c,f"select count(distinct(city)) as c from debug_query where env='{env}' and date(ts)=%s",dt)
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
  
  domain['data'] = date_count_nv(c,f"SELECT domain as ts,count(1) as c from debug_query where env='{env}' and date(ts)=%s group by domain order by c desc ",dt)
  
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
  
  intent['data'] = date_count_nv(c,f"SELECT intents as ts,count(1) as c from debug_query where env='{env}' and date(ts)=%s group by intents order by c desc limit 10",dt)

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
  
  activeUser['data'] = date_count_nv(c,f"SELECT vehicle_id as ts,count(1) as c from debug_query where env='{env}' and date(ts)=%s group by vehicle_id order by c desc limit 20",dt)
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

  r = {'queryCount':queryCount, 'sessionCount':sessionCount, 'onlineSessionCount':onlineSessionCount,'offlineSessionCount':offlineSessionCount, 'cityCount':cityCount,
    'domain':domain, 'intent': intent, 'activeUser':activeUser, 'MonthActiveUser':MonthActiveUser}
  ssdb_save_json(f"{env}.total.info.use_nomi.d.{today.strftime('%Y%m%d')}", r)

def gen_hourly_data(c):
  today = date.today()
  
  queries = date_count(c,f"SELECT hour(ts) as ts,count(1) as c FROM `debug_query` where env='{env}' and date(ts)=%s group by hour(ts)",today.strftime('%Y-%m-%d'))
  hour_query=[0]*24
  for i in queries.keys():
    hour_query[int(i)] = queries[i]
  
  sessiones = date_count(c,f"SELECT hour(ts) as ts,count(distinct(session_id)) as c FROM `debug_query` where env='{env}' and date(ts)=%s group by hour(ts)",today.strftime('%Y-%m-%d'))
  hour_session = [0]*24
  for i in sessiones.keys():
    hour_session[int(i)] = sessiones[i]
 
  vids = date_count(c,f"SELECT hour(ts) as ts,count(distinct(vehicle_id)) as c FROM `debug_query` where env='{env}' and date(ts)=%s group by hour(ts)",today.strftime('%Y-%m-%d')) 
  hour_vid = [0]*24
  for i in vids.keys():
    hour_vid[int(i)] = vids[i]

  #useNomiRate = list(map(truediv, hour_query,hour_vid))
  useNomiRate = [ zdiv(a,b) for a, b in zip(hour_query, hour_vid)]

  domains = get_domains(c)
  
  domainMap = {}
  for d in domains:
    domainMap[d.lower()] = gen_domain(c,d, today)

  r = {'resultMap':{'queryCount':hour_query, 'sessionCount':hour_session,"vidCount":hour_vid, 'useNomiRate':useNomiRate}, 'domainMap':domainMap}
  print(json.dumps(r))
  ssdb_save_json(f"{env}.total.info.use_nomi_hours.d.{today.strftime('%Y%m%d')}", r)

def run_task():
  init()
  db = conn['db']

  with db.cursor() as c:
    gen_hourly_data(c)
    
    today = date.today()
    dt = today.strftime('%Y-%m-%d')
    gen_daily_data(c,dt,today)

if __name__ == '__main__':
  run_task()
