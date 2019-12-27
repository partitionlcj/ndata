import json,pymysql
import pyssdb
import datetime
from config import *

valid_call_intents= set("call_with_name/call_with_org/call_with_num/call_history".split("/"))

def call_path(c, date_range, key, env, detail_info=False):
    c.execute(f"select * from debug_query where env='{env}' and date(ts)>=%s and date(ts)<=%s", date_range)
    rs = c.fetchall()
    call_intent_sessions = set()
    pick_number_sessions = set()
    complete_sessions = set()

    entry_intent_sessions = {}

    for r in rs:
        intents = r.get("intents").split(",")
        sessionId = r.get("session_id")
        for i in intents:
            if i in valid_call_intents:
                #  第一轮
                if sessionId not in call_intent_sessions:
                    if i not in entry_intent_sessions:
                        entry_intent_sessions[i] = set()
                    entry_intent_sessions[i].add(sessionId)

                call_intent_sessions.add(sessionId)
                break

        state = r.get('state')
        if state != None and state == 15:
            pick_number_sessions.add(sessionId)

        operationStr = r.get("operations")
        if operationStr != None:
            operations = operationStr.split(",")
            if 'callNumber' in operations:
                complete_sessions.add(sessionId)

    print(f"len {len(complete_sessions)}")
    call_path_intent(key, call_intent_sessions, pick_number_sessions, complete_sessions, detail_info,env)
    for i in entry_intent_sessions:
        call_path_intent(key+'.'+i, entry_intent_sessions[i], pick_number_sessions, complete_sessions, detail_info,env)


def call_path_intent(key,call_intent_sessions,pick_number_sessions,complete_sessions,detail_info,env):
    s1 = call_intent_sessions.intersection(pick_number_sessions)

    s1_diff = call_intent_sessions.difference(s1)

    s2 = s1.intersection(complete_sessions)

    s2_diff = s1.difference(complete_sessions)

    result = {"1": len(call_intent_sessions), "2": len(s1), "3": len(s2)}

    base_key = f"{env}.call.funnel.{key}"
    ssdb_save_json(base_key, result)
    if detail_info:
        ssdb_save_json(base_key + ".1", list(s1_diff))
        ssdb_save_json(base_key + ".2", list(s2_diff))
        ssdb_save_json(base_key + ".3", list(complete_sessions))

    print(f"{key} 有电话意图 {len(call_intent_sessions)} -> 成功确定号码{len(s1)} -> session执行成功 {len(s2)} ")

if __name__ == '__main__':
    init()
    db = conn['db']

    with db.cursor() as c:
        dt = '2019-03-05'
        call_path(c, (dt, dt), dt, True)
