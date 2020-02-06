import json
import time
import pymysql
from datetime import datetime
from dataclasses import dataclass

@dataclass
class VosReqInfo:
  '''Class for keeping track of an item in inventory.'''
  request_id: str = ''
  session_id: str = ''
  vehicle_id: str = ''
  env: str = ''
  oneshot: bool = False
  car_type: str = ''
  query: str = ''
  tts: str = ''
  view_text: str = ''
  use_cloud_response: bool = False
  operations: str = ''
  start_time: int = -1
  end_time: int = -1
  update_time: datetime = None

  def to_sql_params(self) -> tuple:
    return (self.request_id,  self.session_id, self.vehicle_id, self.env, self.oneshot, self.car_type, self.query, self.tts, self.view_text, self.use_cloud_response, self.operations, self.start_time, self.end_time, self.update_time)

def parse(o, vri):
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
    vri.query = finalResponse.get("query")
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


def vos_ri():
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

  back_time = 31*24*60*60*1000

  ts_end = int(time.time()*1000)
  ts = ts_end - back_time
  

  with db.cursor() as c:
    rids = get_exists_rids(c,ts)
    c.execute("select * from dlg_test.vos_request_info where `update_time`>=%s and `update_time`<%s",(ts,ts_end))
    rs = c.fetchall()
    for r in rs:
      rid = r.get('request_id')
      print(rid)
      if rid not in rids:
        data = r.get("log_data")
        try:
          o = json.loads(data)
        except:
          print(f"fail to parse {data}")
          continue
        vri = VosReqInfo()
        vri.env = r.get("env")
        vri.start_time = r.get("start_time")
        vri.end_time = r.get("end_time")
        vri.update_time = r.get("update_time") / 1000
        parse(o,vri)
        print(vri)
        c.execute("INSERT INTO `vos_debug_query` (`request_id`, `session_id`, `vehicle_id`, `env`, `oneshot`, `car_type`, `query`, `tts`, `view_text`, `use_cloud_response`, `operations`, `start_time`, `end_time`, `update_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s))",vri.to_sql_params() )
  db.commit()


vos_ri()
