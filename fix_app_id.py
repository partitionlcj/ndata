import json
import time
import pymysql
from datetime import datetime

def fix_app_id():
  db = pymysql.connect(
        host='10.25.9.37',
        port=3306,
        user='ais-dev',
        password='QAdr45mfrkled',
        db='sariel',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
  )

  with db.cursor() as c:
    c.execute("select request_id from debug_query where app_id is null")
    rs = c.fetchall()
    for r in rs:
      request_id = r.get('request_id')
      c.execute("select id,input from dialogue.request_info where id=%s",request_id)
      rs = c.fetchall()
      for r in rs:
        rid = r.get('request_id')
        input = r.get('input')
        try:
          o = json.loads(input)
          app_id = o.get('app_id','')
        except:
          print(f"fail to parse {data}")
          continue
      if len(app_id) == 0:
        app_id = ''
      c.execute('update debug_query set app_id=%s where request_id=%s',[app_id, request_id])
      print(request_id)
      db.commit()


fix_app_id()
