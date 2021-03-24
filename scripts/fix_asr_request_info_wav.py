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
        c1.execute("select * from asr_request_info where `timestamp` >= %s", ts)
        rs = c1.fetchall()
        for r in rs:
            rid = r.get('id')
            
            #wd = ssdb_get(rid) 
            #if wd == None or len(wd) == 0:
            if download_wav(rid,r.get('timestamp'),r.get('env')):
                cnt = cnt + 1
                print("download wav " + rid)
    print(f"total {cnt} info processed.")

def download_wav(rid,ts,env):
    provider = 'aws'
    if env == None or env.find('ds-gn') >= 0:
        provider = 'hw'

    if audio_dump(rid,ts,provider):
        pcm2wav(rid)
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
    
    KEY = 'audio_data/'+ dt +'/' + rid 

    try:
        s3.Bucket(bucket).download_file(KEY, 'wav/'+rid)
        return True
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The "+provider+" object "+rid+" does not exist.")
            return False
        else:
            raise

def pcm2wav(rid):
    fn = rid
    p = Popen(["./spx_decoder","wav/"+fn, 'wav/'+fn+".wav"],stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=r'/home/zhouji/app/ndata_di')
    output, err = p.communicate("")
    #print(output)
    #print(err)


def save2ssdb(rid):
    fn = rid 
    with open( 'wav/'+fn + '.wav', 'rb') as wavfile:
        data = wavfile.read()
        ssdb_save(fn,data)
    os.remove('wav/'+fn+".wav")
    os.remove('wav/'+fn)
    
if __name__ == '__main__':
    hour = int(sys.argv[1])
    init()
    pipeline(hour)
    
