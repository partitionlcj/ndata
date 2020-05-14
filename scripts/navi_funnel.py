import json,pymysql
import pyssdb
import datetime
from config import *

valid_nav_intents= set("navi_poi/poi_lookup/navi_favorite/navi_history_go/navi_history_lookup/navi_favorite_list/navi_favorite_list_go".split("/"))
valid_nav_operations = set(["startNavi","callNumber"])

def nav_path(c, date_range, key, env,detail_info=False):
    c.execute(f"select * from debug_query where env='{env}' and date(ts)>=%s and date(ts)<=%s", date_range)
    rs = c.fetchall()
    nav_intent_sessions = set()
    nav_state_resp_sessions = set()
    nav_state_poi_sessions = set()
    nav_operation_sessions = set()

    entry_intent_sessions = {}

    for r in rs:
        intents = r.get("intents").split(",")
        sessionId = r.get("session_id")
        for i in intents:
            if i in valid_nav_intents:
                #  第一轮
                if sessionId not in nav_intent_sessions:
                    if i not in entry_intent_sessions:
                        entry_intent_sessions[i] = set()
                    entry_intent_sessions[i].add(sessionId)

                nav_intent_sessions.add(sessionId)
                break

        state = r.get('state')
        if state != None and state >= 32 and state <= 36:
            nav_state_resp_sessions.add(sessionId)

        if state != None and state in (36, 14, 15):
            nav_state_poi_sessions.add(sessionId)

        operationStr = r.get("operations")
        if operationStr != None:
            operations = operationStr.split(",")
            for o in operations:
                if o in valid_nav_operations:
                    nav_operation_sessions.add(sessionId)
                    break

    calc_by_intent(key,nav_intent_sessions,nav_state_resp_sessions,nav_state_poi_sessions,nav_operation_sessions,detail_info,env)
    for i in entry_intent_sessions:
        calc_by_intent(key+'.'+i, entry_intent_sessions[i], nav_state_resp_sessions, nav_state_poi_sessions, nav_operation_sessions,
                   detail_info,env)


def calc_by_intent(key,entry_intent_sessions,nav_state_resp_sessions,nav_state_poi_sessions,nav_operation_sessions,detail_info,env):
    s1 = entry_intent_sessions.intersection(nav_state_resp_sessions)

    s1_diff = entry_intent_sessions.difference(s1)

    s2 = s1.intersection(nav_state_poi_sessions)

    s2_diff = s1.difference(nav_state_poi_sessions)

    s3 = s2.intersection(nav_operation_sessions)

    s3_diff = s2.difference(nav_operation_sessions)

    result = {"1": len(entry_intent_sessions), "2": len(s1), "3": len(s2),
              "4": len(s3)}

    base_key = f"{env}.nav.funnel.{key}"
    ssdb_save_json(base_key, result)
    if detail_info:
        ssdb_save_json(base_key + ".1", list(entry_intent_sessions))
        ssdb_save_json(base_key + ".2", list(s1_diff))
        ssdb_save_json(base_key + ".3", list(s2_diff))
        ssdb_save_json(base_key + ".4", list(s3_diff))

    print(f"{key}有导航意图 {len(entry_intent_sessions)} -> 成功反馈结果{len(s1)} -> 成功确定了POI {len(s2)} -> session执行成功 {len(s3)} ")

def monthly_result():
    nav_path('2018-08-01', '2018-08-31', 'navi.step_conv.result.monthly.201908')
    nav_path('2018-07-01', '2018-07-31', 'navi.step_conv.result.monthly.201907')


def daily_result():
    dt = '2018-09-17'
    nav_path(dt, dt, 'navi.step_conv.result.daily.' + dt.replace('-', ''), deatil_info=True)

if __name__ == '__main__':
    init()
    db = conn['db']

    with db.cursor() as c:
        dt = '2018-10-08'
        nav_path(c, (dt,dt), dt, True)

