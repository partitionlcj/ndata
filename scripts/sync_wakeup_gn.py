import sys, json, datetime, os
import pymysql
from config import *
import city
import time
import boto3
import botocore
import wave
from db_gn import *
from subprocess import call,Popen,PIPE

rids=set()

def pipeline():
    total_query = 0
    insert_query = 0

    ts = int(time.time()*1000) - 3*60*60*1000

    with conn['db_ri'].cursor() as c1, conn['db'].cursor() as c2:
        c1.execute("select * from wakeup_info where `timestamp` >= %s", ts)
        rs = c1.fetchall()
        for r in rs:
            rid = r.get('id')
            asr_text = r.get('asr_text')
            if asr_text != None:
                asr_text = asr_text.upper()
            wd = ssdb_get('WAKEUP_'+rid) 
            if wd == None or len(wd) == 0:
                if download_wav(rid,r.get('timestamp'),r.get('env')):
                    c2.execute('update debug_query set wakeup=1,wakeup_asr_text=%s where request_id=%s',[asr_text,rid])
                    conn['db'].commit()
                    print("sync ri status " + rid)
            else:
                c2.execute('select wakeup_asr_text from debug_query where request_id=%s',rid)
                rs = c2.fetchone()
                if rs != None:
                    wat = rs.get('wakeup_asr_text')
                    if wat == None or len(wat) == 0 :
                        c2.execute('update debug_query set wakeup=1,wakeup_asr_text=%s where request_id=%s',[asr_text,rid])
                        c2.execute('update vos_debug_query set wakeup=1,wakeup_asr_text=%s where request_id=%s',[asr_text,rid])
                        conn['db'].commit()
                        print("[fix] sync ri status " + rid)

            rids.add(rid)
    print(f"total {len(rids)} wakeup info processed.")

def download_wav(rid,ts,env):
    provider = 'aws'
    if env == None or env.find('ds-gn') >= 0:
        provider = 'hw'

    if audio_dump(rid,ts,provider):
        #pcm2wav(rid)
        save2ssdb(rid)
        return True
    else:
        return False

def audio_dump(rid, ts, provider='aws'):
    dt = datetime.datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d')

    bucket = 'ais-storage-gz'
    s3 = boto3.resource(
                's3',
                aws_access_key_id='EPYG0BBE0O37MORZ8WGE',
                aws_secret_access_key='BFoQLLDiBELjZMndiRLj8ZprF4XoKDMBHqYZO70R',
                endpoint_url='http://obs.cn-south-1.myhuaweicloud.com/'
                )
    KEY = 'audio_data/'+ dt +'/WAKEUP_' + rid + '.wav'

    try:
        s3.Bucket(bucket).download_file(KEY, 'WAKEUP_'+rid+'.wav')
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The "+provider+" weakup object "+rid+" does not exist.")
            return False
        else:
            raise

def pcm2wav(rid):
    fn = 'WAKEUP_' + rid 
    p = Popen(["./SpeexToPcm",fn+'.pcm', fn+".wav"],stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=r'/data/app/mars-ndata')
    output, err = p.communicate("")
    print(output)
    print(err)

def save2ssdb(rid):
    fn = 'WAKEUP_' + rid 
    with open( fn + '.wav', 'rb') as wavfile:
        data = wavfile.read()
        ssdb_save(fn,data)
        if ssdb_get(rid) == None:
            print(f"{rid} only has wakup wav.")
    #os.remove(fn+'.pcm')
    os.remove(fn+".wav")
    

if __name__ == '__main__':
    init()
    pipeline()
    
    
