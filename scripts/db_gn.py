import pymysql
import pyssdb

def init():
    conn['ssdb'] = pyssdb.Client(host='k8s-ssdb-svc',port=8888)
    conn['db'] = pymysql.connect(
        host='172.25.5.222',
        port=3306,
        user='report_w',
        password='btp9PrtDamlE2Qzv',
        db='report_stg',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )

    conn['db_ri'] = pymysql.connect(
        host='172.25.5.222',
        port=3306,
        user='dialogue_w',
        password='q6reOxw3fg5wZiDz',
        db='dialogue_stg',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
    )