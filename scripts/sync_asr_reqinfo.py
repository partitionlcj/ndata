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
    if conn['ssdb'].get(rid) != None:
        print('skip')
        return

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

def pcm2wav1(rid):
    with open(rid, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open( rid + '.wav', 'wb') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)

def save2ssdb(rid):
    with open( rid + '.wav', 'rb') as wavfile:
        data = wavfile.read()
        ssdb_save(rid,data)
        print("add wav "+rid)
    os.remove(rid)
    os.remove(rid+".wav")
    

if __name__ == '__main__':
    init()
    db = conn['db']
    db_ri = conn['db_ri']
    hour = int(sys.argv[1])
    asr_pipeline(hour)
    
    
