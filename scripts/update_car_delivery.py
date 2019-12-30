from config import *

init()
with conn['db'].cursor() as c:
  c.execute("replace into car_delivery (vehicle_id,activate_time,env) select vehicle_id,min(ts),min(env) from debug_query where length(vehicle_id) = 32 group by vehicle_id")
  conn['db'].commit()