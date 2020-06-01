import pymysql
import pyssdb

def init():
    #conn['ssdb'] = pyssdb.Client(host='10.86.11.20',port=31120)
    conn['ssdb'] = pyssdb.Client(host='10.25.9.37',port=13231)
    conn['db'] = pymysql.connect(
        host='10.25.9.37',
        port=3306,
        user='ndata',
        password='dsfEncr43slf',
        db='sariel',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )

    conn['db_ri'] = pymysql.connect(
        host='10.25.9.37',
        port=3306,
        user='ais-dev',
        password='QAdr45mfrkled',
        db='dialogue',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )