import json
import time, sys
import pymysql
from datetime import datetime

class VosReqInfo:
  '''Class for keeping track of an item in inventory.'''
  request_id: str = ''
  session_id: str = ''
  vehicle_id: str = ''
  env: str = ''
  city: str = ''
  province: str = ''
  oneshot: bool = False
  car_type: str = ''
  query: str = ''
  vossdk_ver: str = ''
  tts: str = ''
  view_text: str = ''
  use_cloud_response: bool = False
  operations: str = ''
  start_time: int = -1
  end_time: int = -1
  duration: int = 0
  update_time: datetime = None
  domain: str = ''
  intents: str = ''
  wakeup: int = 0
  wakeup_asr_text: str = ''
  app_id:str = ''

  def to_sql_params(self) -> tuple:
    return (self.request_id,  self.session_id, self.vehicle_id, self.env, self.oneshot, self.car_type, self.query, self.tts, self.view_text, self.use_cloud_response, self.operations, self.start_time, self.end_time, self.duration, self.update_time, self.domain, self.intents, self.wakeup, self.wakeup_asr_text,self.app_id, self.city, self.province, self.vossdk_ver)

def parse(o, vri):
  ver = o.get('versions')
  if ver != None:
    vri.vossdk_ver = ver.get('vos_sdk_release')
    if vri.vossdk_ver == None:
        vri.vossdk_ver = ver.get('vossdk','N/A')
  asrNluRequestHeader = o.get('asrNluRequestHeader')
  if asrNluRequestHeader != None:
    vri.request_id = asrNluRequestHeader.get("id","")
    vri.vehicle_id = asrNluRequestHeader.get("vehicleId","")
    vri.oneshot = asrNluRequestHeader.get("oneshot",False)
    extra = asrNluRequestHeader.get("extra")
    if extra != None:
      vri.car_type = extra.get("carType","")

  dialogueRequestBody = o.get("dialogueRequestBody")

  finalResponse =o.get("finalResponse")
  if finalResponse != None:
    vri.query = finalResponse.get("query",'')
    vri.session_id = finalResponse.get("sessionId","")

    tts = finalResponse.get("tts")
    if tts != None:
      vri.tts = json.dumps(tts,ensure_ascii=False)
    
    view = finalResponse.get("view")
    if view != None:
      vri.view = json.dumps(view,ensure_ascii=False)

    operations = finalResponse.get("operations")
    if operations != None:
      vri.operations = json.dumps(operations)

  finalAsrResult = o.get('finalAsrResult')
  if finalAsrResult != None and vri.query == '' :
    vri.query = finalAsrResult.get('online_result','')
    if vri.query == '':
      vri.query = finalAsrResult.get('offline_result','')
  
  vri.use_cloud_response = o.get("isUsingCloudResponse")

def test():
  with open('/Users/sonsonk/mega/sample.json','r') as f:
    o = json.load(f)
    vri = VosReqInfo()
    parse(o,vri)
    print(vri)

def get_exists_rids(c,ts):
  c.execute("select request_id from sariel.vos_debug_query where `update_time`>= FROM_UNIXTIME(%s)", (ts / 1000 - 1000))
  rs = c.fetchall()

  pnq_ids = set()
  for r in rs:
    pnq_ids.add(r.get('request_id'))
  return pnq_ids


def vos_ri(hour):
  db = pymysql.connect(
        host='10.25.9.37',
        port=3306,
        user='ais-dev',
        password='QAdr45mfrkled',
        db='sariel',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
  )
  total_query = 0
  insert_query = 0

  back_time = int(hour)*60*60*1000

  ts_end = int(time.time()*1000)
  ts = ts_end - back_time

  with db.cursor() as c:
    rids = get_exists_rids(c,ts)
    c.execute("select * from dialogue.vos_request_info where `update_time`>=%s and `update_time`<%s order by update_time asc",(ts,ts_end))
    rs = c.fetchall()
    print(f"fetch {len(rs)} vod_request_info records")
    for r in rs:
      rid = r.get('request_id')
      if rid not in rids:
        data = r.get("log_data")
        try:
          o = json.loads(data)
          o1 = o.get('asrNluRequestHeader',None)
          if o1 != None:
            extra = o1.get('extra',None)
            if extra != None:
              app_id = extra.get('appId','')
        except:
          print(f"fail to parse {data}")
          continue
        vri = VosReqInfo()
        vri.request_id = rid
        vri.env = r.get("env")
        vri.start_time = r.get("start_time")
        vri.end_time = r.get("end_time")
        vri.duration = vri.end_time - vri.start_time
        vri.update_time = r.get("update_time") / 1000
        parse(o,vri)
        print(rid + " - " + str(vri.query))
        c.execute('select domain,intents,wakeup,wakeup_asr_text,app_id,city,province from debug_query where request_id=%s',(rid))
        rr = c.fetchone()
        if rr != None:
            vri.domain = rr.get('domain','')
            vri.intents = rr.get('intents','')
            vri.wakeup = rr.get('wakeup')
            vri.city = rr.get('city')
            vri.province = rr.get('province')
            vri.wakeup_asr_text = rr.get('wakeup_asr_text','')
            if vri.app_id == '':
              vri.app_id = rr.get('app_id','')
        #print(vri.to_sql_params())
        if len( vri.query ) > 768:
            print("query too long: " + rid + " - " + str(vri.query))
            continue
        c.execute("REPLACE INTO `vos_debug_query` (`request_id`, `session_id`, `vehicle_id`, `env`, `oneshot`, `car_type`, `query`, `tts`, `view_text`, `use_cloud_response`, `operations`, `start_time`, `end_time`, duration, `update_time`,domain,intents,wakeup,wakeup_asr_text,app_id,city,province,vossdk_ver) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s),%s,%s, %s, %s,%s,%s,%s, %s)",vri.to_sql_params() )
  db.commit()
  print("vos di complete")

hours = int(sys.argv[1])
vos_ri(hours)
