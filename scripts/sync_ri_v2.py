import sys, json, datetime, os
import pymysql
from config import *
import city
import time
import boto3
import botocore
import wave
from subprocess import call,Popen,PIPE

BUCKET_NAME = 'ais-storage'

class HuDataTracking(object):
    def __init__(self):
        self.id = ''
        self.request_id = ''
        self.vehicle_id = ''
        self.session_id = ''
        self.user_id = ''
        self.query = ''
        self.final_tts = ''
        self.final_view_text = ''
        self.ts = 0
        self.domain = ''
        self.intents = ''
        self.env = ''
        self.nlu_type = -1
        self.multi_round = 0
        self.city = ''
        self.address = ''
        self.request_trigger_by = 0
        self.use_response = 0
        self.awaken_type = 0
        self.sound_location = ''
        self.state = -1
        self.operations = ''
        self.catemr = ''
        self.client_version = ''
        # 连续对话id
        self.cst_id = ''
        # 内部版本号	ES8.0.5.33.0096_190115A2.2.2
        self.sd_ver = ''
        self.query_inhouse = ''
        self.use_inhouse = ''
        self.voice_id = 0
        self.output = ''

    def get_req_infos(self, r):
        if r != None:
            self.merge_request_info(r)
        else:
            print(f"{self.rid} not found!")


    def proc_tts(self, o):
        r = []
        if o == None or o.get('tts') == None:
            return '[]'
        return json.dumps(o.get('tts'),ensure_ascii=False)

    def proc_view_text(self, o):
        r = []
        if o == None or o.get('view') == None or o.get('view').get('viewTextV2') == None:
            return '[]'
        return json.dumps(o.get('view').get('viewTextV2'),ensure_ascii=False)

    def proc_nlu_type(self, o):
        if o == None or o.get('ttsV2') == None:
            return 0
        for i in o.get('ttsV2'):
            id = str(i.get('id'))
            if id in type1:
                return 1
            elif id in type1_with_intents:
                if len(set(self.intents).intersection(type1_intents)) > 0:
                    return 1
                elif len(set(self.intents).intersection(type2_intents)) == 0:
                    return 2
            elif id in type3:
                return 3
        return 0

    def proc_catemr(self, ri):
        sstr = ri.get('server_state')

        dialogueDecison = None
        if sstr != None:
            ss = json.loads(sstr)
            dialogueDecison = ss.get('dialogueDecison', None)

        if dialogueDecison == None:
            mrstr = ri.get('model_results')
            if mrstr != None:
                mr = json.loads(mrstr)
                if mr == None or 'classificationModelResult' not in mr:
                    dialogueDecison = 'unknown'
                else:
                    cate = str(mr.get('classificationModelResult').get('type'))
                    if cate in cates:
                        dialogueDecison = cates[cate]
                    else:
                        print(f"error cate {cate}")
                        dialogueDecison = cate
        return dialogueDecison

    def merge_request_info(self, ri):
        self.request_id = ri['id']
        self.session_id = ri['session_id']
        self.user_id = ri['user_id']
        self.vehicle_id = ri['vehicle_id']
        self.env = ri['env']
        self.query = ri['query']

        if self.query == None:
            self.query = 'N/A'

        self.output = ri['output']
        self.client_version = ri['client_version']
        if self.client_version != None:
            self.client_version = self.client_version.replace('"', '')

        # ssdb_save("vid.client_version." + self.vehicle_id, self.client_version)

        #if self.query == None or len(self.query) == 0:
        #    return
        # self.ts= datetime.datetime.fromtimestamp(ri['timestamp']/1000).isoformat()
        self.ts = ri['timestamp'] / 1000
        r = json.loads(ri['nlu_result'])
        if r != None:
            self.domain = r.get('domain', '')

        input = json.loads(ri['input'])
        self.query_inhouse = input.get('queryInhouse',None)
        self.oneshot = input.get('oneshot', None)

        extra = input.get('extra',{})
        self.voice_id = int(extra.get('voiceId',0))
        self.sd_ver = extra.get('sdVer',None)
        self.sound_location = extra.get('soundLocation',None)

        if r != None and 'intentList' in r and len(r['intentList']) > 0:
            intents = ''
            for i in r['intentList']:
                if len(intents) == 0:
                    intents = i['type']
                else:
                    intents = intents + ',' + i['type']
            self.intents = intents
        else:
            self.intents = ''

        output = json.loads(ri['output'])
        self.nlu_type = self.proc_nlu_type(output)

        self.final_tts = self.proc_tts(output)
        self.final_view_text = self.proc_view_text(output)

        self.catemr = self.proc_catemr(ri)

        if output != None:
            self.state = output.get('state', -1)
            operations = output.get('operations')

            opTypes = []
            for oper in operations:
                opTypes.append(oper.get('type'))

            self.operations = ",".join(opTypes)

        if r != None and  'multiRoundLabel' in r and r['multiRoundLabel']:
            self.multi_round = 1

        ss = json.loads(ri['server_state'])

        self.cst_id = ss.get("cstDialogId",None)

        l = ss.get('location', None)
        self.city = ss.get('curCity', '')

        if l:
            if 'curCity' in l :
                self.city = l.get('curCity', '')
            else:
                ll = l.split(",")
                ct = city.get_city(float(ll[0]),float(ll[1]))
                if self.city != '' and self.city != ct:
                    print(f"{self.city} != {ct}, l={l}")
                self.city = ct

        self.save_db()

    def save_db(self):
        with db.cursor() as c:
            c.execute(
                "REPLACE INTO debug_query (request_id, vehicle_id, session_id, user_id, query,nlu_type, final_tts, final_view_text, ts, domain, intents,multi_round,env,city,address,request_trigger_by,use_response,awaken_type,sound_location,state,operations,catemr,cst_id,client_version,sd_ver, inhouse_query, oneshot, voice_id, output) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                (self.request_id, self.vehicle_id, self.session_id, self.user_id, self.query, self.nlu_type,
                 self.final_tts, self.final_view_text, self.ts, self.domain, self.intents, self.multi_round, self.env,
                 self.city, self.address, self.request_trigger_by, self.use_response, self.awaken_type,
                 self.sound_location, self.state, self.operations, self.catemr, self.cst_id, self.client_version,
                 self.sd_ver, self.query_inhouse, self.oneshot, self.voice_id, self.output))
            db.commit()

def process_vid_file(fn):
    with open(fn, 'r') as fp:
        for line in fp:
            hdt = HuDataTracking()
            hdt.get_req_infos(line.replace('\n', ''))

def get_exist_rids(c,ts):
    c.execute("select request_id from debug_query where ts >= FROM_UNIXTIME(%s)",
               (ts / 1000 - 1000))
    rs2 = c.fetchall()

    pnq_ids = set()
    for r2 in rs2:
        pnq_ids.add(r2.get('request_id'))
    return pnq_ids

'''
1. 获取起始时间(3天前）
2. 获取 debug_query表中对应的id
3. 获取实车vid和激活ts
4. 获取request_info起始时间开始的数据，对每条数据检查vid和ts，分析是否是有效数据；
'''
def pipeline():
    total_query = 0
    insert_query = 0

    back_time = 7*24*60*60*1000

    ts_end = int(time.time()*1000) 
    ts = ts_end - back_time
    vid_ts = {}

    with db_ri.cursor() as c1, db.cursor() as c2:
        rids = get_exist_rids(c2,ts)
        print(f"{len(rids)} already inserted.")
        print("select * from request_info where `timestamp`>=%s and `timestamp`<%s",(ts,ts_end))
        c1.execute("select * from request_info where `timestamp`>=%s and `timestamp`<%s",(ts,ts_end))
        rs1 = c1.fetchall()

        for r1 in rs1:
            rid = r1.get('id')
            vid = r1.get('vehicle_id')
            env = r1.get('env')
            ts2 = r1.get('timestamp')
            total_query += 1

            if rid not in rids: #and  and :
                hdt = HuDataTracking()

                print(rid)
                hdt.get_req_infos(r1)
                insert_query += 1

                provider = 'aws'
                if env.find('ds-gn') >= 0:
                    provider = 'hw'

                if audio_dump(rid,ts2,provider):
                    pcm2wav(rid)
                    save2ssdb(rid)

        print(f"total {total_query} queries, insert {insert_query} queries")

def audio_dump(rid, ts, provider='aws'):
    dt = datetime.datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d')
    bucket = BUCKET_NAME

    if provider == 'hw':
        bucket = 'ais-storage-gz'
        print('hw')
        s3 = boto3.resource(
                    's3',
                    aws_access_key_id='EPYG0BBE0O37MORZ8WGE',
                    aws_secret_access_key='BFoQLLDiBELjZMndiRLj8ZprF4XoKDMBHqYZO70R',
                    endpoint_url='http://obs.cn-south-1.myhuaweicloud.com/'
                  )
    else:
        s3 = boto3.resource('s3')
    
    KEY = 'audio_data/'+ dt +'/' + rid

    try:
        print(KEY)
        s3.Bucket(bucket).download_file(KEY, rid)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The "+provider+" object does not exist.")
            return False
        else:
            raise

def pcm2wav(rid):
    fn = rid
    p = Popen(["./SpeexToPcm",fn, fn+".wav"],stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=r'/home/zhouji/app/ndata_di')
    output, err = p.communicate("")
    print(output)
    print(err)

def pcm2wav1(rid):
    with open(rid, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open( rid + '.wav', 'wb') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)

def save2ssdb(rid):
    with open( rid + '.wav', 'rb') as wavfile:
        data = wavfile.read()
        print(rid+".wav")
        ssdb_save(rid,data)
    os.remove(rid)
    os.remove(rid+".wav")
    

if __name__ == '__main__':
    init()
    db = conn['db']
    db_ri = conn['db_ri']

    pipeline()
    
    
