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
    c.execute("select request_id from vos_debug_query")
    rs = c.fetchall()
    i = 0
    for r in rs:
      ver = ''
      request_id = r.get('request_id')
      c.execute("select log_data from dialogue.vos_request_info where request_id=%s",request_id)
      r = c.fetchone()
      if r == None:
        continue
      input = r.get('log_data')
      try:
        o = json.loads(input)
        o1 = o.get('versions',None)
        if o1 != None:
          ver = o1.get('vos_sdk_release')
          if ver == None:
            ver = o1.get('vos_sdk_release ')  
          if ver == None:
            ver = o1.get('vossdk','N/A')  
      except:
        print(f"fail to parse {o}")
        continue
     
      c.execute('update vos_debug_query set vossdk_ver=%s where request_id=%s',[ver, request_id])
      i = i +1 
      if i % 10 == 0:
        db.commit()
      print(request_id +'\t'+ver)
    db.commit()


fix_app_id()
