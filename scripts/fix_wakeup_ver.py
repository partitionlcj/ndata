import json
import time
import pymysql
from datetime import datetime

def fix_ver():
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
    c.execute("select id from wakeup_info where vossdk_ver is null or vossdk_ver = ''")
    rs = c.fetchall()
    for r in rs:
      ver = ''
      request_id = r.get('id')
      c.execute("select log_data from vos_request_info where request_id=%s",request_id)
      r = c.fetchone()
      if r == None:
        continue
      input = r.get('log_data')
      try:
        o = json.loads(input)
        o1 = o.get('versions',None)
        if o1 != None:
          ver = o1.get('vossdk','N/A')
      except:
        print(f"fail to parse {o}")
        continue
     
      c.execute('update wakeup_info set vossdk_ver=%s where id=%s',[ver, request_id])
      print(request_id)
      db.commit()


fix_ver()
