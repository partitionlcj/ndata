import wave
from subprocess import call,Popen,PIPE
import sys, json, datetime, os
import pymysql
from config import *
import time
import boto3
import botocore

BUCKET_NAME = 'ais-storage'

def audio_dump(rid, ts, provider='aws'):
    dt = datetime.datetime.fromtimestamp(ts/1000).strftime('%Y-%m-%d')
    KEY = 'audio_data/'+ dt +'/' + rid

    if conn['ssdb'].get(rid) != None:
        print('skip')
        return
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

def save2ssdb(rid):
    with open( rid + '.wav', 'rb') as wavfile:
        data = wavfile.read()
        print(rid+".wav")
        ssdb_save(rid,data)
    os.remove(rid)
    os.remove(rid+".wav")

def dump_wav_to_ssdb(env,rid):
    provider = 'aws'
    if env.find('ds-gn') >= 0:
        provider = 'hw'

    if audio_dump(rid,ts2,provider):
        pcm2wav(rid)
        save2ssdb(rid)