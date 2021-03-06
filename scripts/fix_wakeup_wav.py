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

rids=set()

def pipeline(hour):
    cnt = 0

    ts = int(time.time()*1000) - hour*60*60*1000

    with conn['db_ri'].cursor() as c1, conn['db'].cursor() as c2:
        c1.execute("update wakeup_info set sdk_version='' where sdk_version is null")
        conn['db_ri'].commit()
        c1.execute("select * from wakeup_info where `timestamp` >= %s", ts)
        rs = c1.fetchall()
        for r in rs:
            rid = r.get('id')
            
            wd = ssdb_get('WAKEUP_'+rid) 
            if wd == None or len(wd) == 0:
                if download_wav(rid,r.get('timestamp'),r.get('env')):
                    cnt = cnt + 1
                    print("download wakeup wav " + rid)
    print(f"total {cnt} wakeup info processed.")

def download_wav(rid,ts,env):
    provider = 'aws'
    if env == None or env.find('ds-gn') >= 0:
        provider = 'hw'

    if audio_dump(rid,ts,provider):
        save2ssdb(rid)
        return True
    else:
        return False

def audio_dump(rid, ts, provider='aws'):
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

def save2ssdb(rid):
    fn = 'WAKEUP_' + rid 
    with open( fn + '.wav', 'rb') as wavfile:
        data = wavfile.read()
        ssdb_save(fn,data)
        if ssdb_get(rid) == None:
            print(f"{rid} only has wakup wav.")
    os.remove(fn+".wav")
    
if __name__ == '__main__':
    hour = int(sys.argv[1])
    init()
    pipeline(hour)
    
