import sys, json, datetime, os
import pymysql
from config import *
import city
import time
import boto3
import botocore
import wave


BUCKET_NAME = 'ais-storage'

rids=set()

def pipeline():
    total_query = 0
    insert_query = 0

    ts = int(time.time()*1000) - 7*24*60*60*1000

    with db.cursor() as c:
        c.execute("select id,env,`timestamp` from dialogue.wakeup_info where `timestamp` >= %s", ts)
        rs = c.fetchall()
        for r in rs:
            rid = r.get('id')
            if ssdb_get('WAKEUP_'+rid) == None:
                download_wav(rid,r.get('timestamp'),r.get('env'),c)
            rids.add(rid)
    db.commit()
    print(f"total {len(rids)} wakeup info processed.")

def download_wav(rid,ts,env,c):
    provider = 'aws'
    if env.find('ds-gn') >= 0:
        provider = 'hw'

    if audio_dump(rid,ts,provider):
        pcm2wav(rid)
        save2ssdb(rid)
        c.execute('update debug_query set wakeup=1 where request_id=%s',rid)

def audio_dump(rid, ts, provider='aws'):
    dt = datetime.datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d')
    bucket = BUCKET_NAME

    if provider == 'hw':
        bucket = 'ais-storage-gz'
        print('hw')
        s3 = boto3.resource(
                    's3',
                    aws_access_key_id='NQBXVLYGNC5ZAL6WLHQV',
                    aws_secret_access_key='fD0f9rCHd3fAYl0bewgoZI7VyxO4hp1e4BasEoJW',
                    endpoint_url='http://obs.cn-south-1.myhuaweicloud.com/'
                  )
    else:
        s3 = boto3.resource('s3')
    
    KEY = 'audio_data/'+ dt +'/WAKEUP_' + rid

    try:
        print(KEY)
        s3.Bucket(bucket).download_file(KEY, 'WAKEUP_'+rid)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The "+provider+" object does not exist.")
            return False
        else:
            raise

def pcm2wav(rid):
    fn = 'WAKEUP_' + rid
    with open(fn, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open( fn + '.wav', 'wb') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)

def save2ssdb(rid):
    fn = 'WAKEUP_' + rid
    with open( fn + '.wav', 'rb') as wavfile:
        data = wavfile.read()
        print(fn+".wav")
        ssdb_save(fn,data)
        if ssdb_get(rid) == None:
            print(f"{rid} only has wakup wav.")
    os.remove(fn)
    os.remove(fn+".wav")
    

if __name__ == '__main__':
    init()
    db = conn['db']

    pipeline()
    
    
