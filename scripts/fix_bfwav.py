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
        self.app_id = ''
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
        self.province= ''
        self.request_trigger_by = 0
        self.use_response = 0
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
        self.continuous_dialog = False
        self.bfwav = 0

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
        self.app_id = input.get('app_id', None)
       

        q = input.get("query",None)
        if q != None and self.query != 'N/A' and  q != self.query:
            print("[Fix] find query correction, original query is " + q)
            self.query = self.query + "^" + q

        extra = input.get('extra',{})
        self.voice_id = int(extra.get('voiceId',0))
        self.sd_ver = extra.get('sdVer',None)
        self.sound_location = extra.get('soundLocation',None)
        self.continuous_dialog = extra.get("continuousDialog",False)
        if self.continuous_dialog == 'true':
            self.continuous_dialog = True
        if self.continuous_dialog == 'false':
            self.continuous_dialog = False

        if r != None and 'intentList' in r and len(r['intentList']) > 0:
            intents = ''
            for i in r['intentList']:
                if len(intents) == 0:
                    intents = i.get('type','')
                else:
                    intents = intents + ',' + i.get('type','')
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
        self.province = ss.get('province', '')

        if l:
            if 'curCity' in l :
                self.city = l.get('curCity', '')
                self.province = l.get('province', '')
            else:
                ll = l.split(",")
                ct = city.get_city(float(ll[0]),float(ll[1]))
                if self.city != '' and self.city != ct.get('name'):
                    print(f"{self.city} != {ct}, l={l}")
                self.city = ct.get('name')
                self.province = ct.get('province')

    def save_db(self):
        with db.cursor() as c:
            c.execute(
                "REPLACE INTO debug_query (request_id, vehicle_id, session_id, user_id, query,nlu_type, final_tts, final_view_text, ts, domain, intents,multi_round,env,city,province,request_trigger_by,use_response,sound_location,state,operations,catemr,cst_id,client_version,sd_ver, inhouse_query, oneshot, voice_id, output, app_id,continuous_dialog,bfwav) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, FROM_UNIXTIME(%s), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)",
                (self.request_id, self.vehicle_id, self.session_id, self.user_id, self.query, self.nlu_type,
                 self.final_tts, self.final_view_text, self.ts, self.domain, self.intents, self.multi_round, self.env,
                 self.city, self.province, self.request_trigger_by, self.use_response, 
                 self.sound_location, self.state, self.operations, self.catemr, self.cst_id, self.client_version,
                 self.sd_ver, self.query_inhouse, self.oneshot, self.voice_id, self.output, self.app_id, self.continuous_dialog,self.bfwav))
            print(self.request_id)
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


    ts_end = int(time.time()*1000) 
    vid_ts = {}

    with db_ri.cursor() as c1, db.cursor() as c2:
        rids = [] #get_exist_rids(c2,ts)
        print(f"{len(rids)} already inserted.")
        c1.execute("select * from request_info where id='906b6f68-bcf2-4b87-991b-0f861bdb4993'")
        rs1 = c1.fetchall()

        for r1 in rs1:
            rid = r1.get('id')
            vid = r1.get('vehicle_id')
            env = r1.get('env')
            ts2 = r1.get('timestamp')
            total_query += 1

            if rid not in rids: #and  and :
                hdt = HuDataTracking()

                hdt.get_req_infos(r1)
                insert_query += 1

                provider = 'aws'
                if env.find('ds-gn') >= 0:
                    provider = 'hw'

                if audio_dump(rid,ts2,provider):
                    pcm2wav(rid)
                    save2ssdb(rid)
                    bfwav(rid,ts2,provider,hdt)

                hdt.save_db()

        print(f"total {total_query} queries, insert {insert_query} queries")

def bfwav(rid,ts2,provider,hdt):
  check_bfwav(rid,ts2,provider,1,0,hdt)
  #check_bfwav(rid,ts2,provider,1,1,hdt)
  check_bfwav(rid,ts2,provider,4,0,hdt)
  #check_bfwav(rid,ts2,provider,4,1,hdt)

def check_bfwav(rid,ts2,provider,channel,useSpeex,hdt):
  nRid = f"{rid}_{channel}_{useSpeex}"
  if audio_dump(nRid,ts2,provider):
    if channel == 1:
      pcm2wav(nRid)
    else:
      pcm2wav_4channel(nRid)
    save2ssdb2(f"{rid}_{channel}", nRid)
    hdt.bfwav = hdt.bfwav + channel

def asr_pipeline(hour):
    back_time = hour*60*60*1000

    ts_end = int(time.time()*1000) 
    ts = ts_end - back_time

    wav_num = 0

    with db_ri.cursor() as c1:
        c1.execute("select * from asr_request_info where `timestamp`>=%s and `timestamp`<%s",(ts,ts_end))
        rs1 = c1.fetchall()

        for r1 in rs1:
            rid = r1.get('id')
            app_id = r1.get('app_id')
            env = r1.get('env')
            ts2 = r1.get('timestamp')
            env = r1.get('env')

            if env.find('dev') >=0 or env.find("int") > 0:
                if app_id != '100990130':
                    continue
            
            provider = 'aws'
            if env.find('ds-gn') >= 0:
                provider = 'hw'

            if audio_dump(rid,ts2,provider):
                pcm2wav(rid)
                save2ssdb(rid)
                wav_num = wav_num + 1

        print(f"{wav_num} asr wav imported.")

def audio_dump(rid, ts, provider='aws'):
    #if conn['ssdb'].get(rid) != None:
    #    print('skip')
    #    return

    dt = datetime.datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d')
    bucket = BUCKET_NAME

    if provider == 'hw':
        bucket = 'ais-storage-gz'
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
    p = Popen(["./spx_decoder",fn, fn+".wav"],stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=r'/home/zhouji/app/ndata_di')
    output, err = p.communicate("")
    #print(output)
    #print(err)

def pcm2wav_4channel(rid):
    with open(rid, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open( rid + '.wav', 'wb') as wavfile:
        wavfile.setparams((4, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)

def save2ssdb(rid):
    with open( rid + '.wav', 'rb') as wavfile:
        data = wavfile.read()
        ssdb_save(rid,data)
        print("add wav "+rid)
    os.remove(rid)
    os.remove(rid+".wav")

def save2ssdb2(key,fn):
    with open( fn + '.wav', 'rb') as wavfile:
        data = wavfile.read()
        ssdb_save(key,data)
        print("add wav "+key)
    os.remove(fn)
    os.remove(fn+".wav")
    print(f"save {fn} to key")

if __name__ == '__main__':
    init()
    db = conn['db']
    db_ri = conn['db_ri']
    pipeline()
    #bfwav('906b6f68-bcf2-4b87-991b-0f861bdb4993',1615968768168,'hw',hdt)


