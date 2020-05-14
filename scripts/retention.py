import json
from config import *
from datetime import date,datetime,timedelta

def get_dau_vids(dt):
    d = dt.strftime('%Y%m%d')
    k = f'{env}.base.active_vids.d.' + d
    return get_set_from_ssdb(k)

def get_dnu_vids(dt):
    d = dt.strftime('%Y%m%d')
    k = 'base.new_vids.d.' + d
    return get_set_from_ssdb(k)

def get_wau_vids(monday):
    k = f'base.active_vids.' + get_week_key(monday)
    return get_set_from_ssdb(k)

def get_wnu_vids(monday):
    k = f'base.new_vids.' + get_week_key(monday)
    return get_set_from_ssdb(k)

def get_wau_vids(monday):
    k = f'base.active_vids.' + get_week_key(monday)
    return get_set_from_ssdb(k)

def get_mnu_vids(year,month):
    k = f'base.new_vids.' + get_month_key(year, month)
    return get_set_from_ssdb(k)

def get_mau_vids(year,month):
    k = f'base.active_vids.'+get_month_key(year,month)
    return get_set_from_ssdb(k)

def retention_daily(dt, dau, days_before):
    dnu = get_dnu_vids(dt - timedelta(days=days_before))
    if dnu == None or len(dnu) == 0:
        return 'N/A'
    r = float(len(dau.intersection(dnu))) / len(dnu)
    return '{:.2%}'.format(r)

def retention_weekly(monday, wau, weeks_before):
    wnu = get_wnu_vids(monday - timedelta(days=weeks_before*7))
    if wnu == None:
        return 'N/A'
    r = float(len(wau.intersection(wnu))) / len(wnu)
    return '{:.2%}'.format(r)

def retention_monthly(mau,year,month,month_before):
    (y,m) = get_month_before(year,month,month_before)
    mnu = get_mnu_vids(y,m)
    if mnu == None:
        return 'N/A'
    r = float(len(mau.intersection(mnu))) / len(mnu)
    return '{:.2%}'.format(r)

def daily(dt):
    # active user
    dau = get_dau_vids(dt)
    retentions_daily = {}
    for i in [0,1,3,7,30,60]:
        if i == 0:
            retentions_daily["当日新用户激活率"]=retention_daily(dt, dau, i)
        else:
            retentions_daily[str(i) + "天前用户留存"] = retention_daily(dt, dau, i)
    ssdb_save('retention.d.'+dt.strftime('%Y%m%d'),retentions_daily)

def weekly(monday):
    wau = get_wau_vids(monday)
    retentions_weekly = {}
    for i in range(0,8):
        k = str(i)+"周前用户留存"
        if i == 0:
            k = "本周新用户激活率"
        retentions_weekly[k]=retention_weekly(monday,wau,i)
    print(retentions_weekly)
    ssdb_save('retention.' + get_week_key(monday),retentions_weekly)

def monthly(year,month):
    mau = get_mau_vids(year,month)
    r = {}
    for i in range(0, 5):
        k = str(i)+"月前用户留存"
        if i == 0:
            k = "本月新用户激活率"
        r[k] = retention_monthly(mau, year,month, i)
    ssdb_save('retention.' + get_month_key(year,month), r)

    detail_retention(year, month)

def get_month_before(year,month,month_before):
    if month_before >= 12:
        raise Exception('month_before is too large!')
    if month <= month_before:
        return (year-1,12 + month - month_before)
    else:
        return (year,month-month_before)

def get_new_vids_before(dt):
    with conn['db'].cursor() as c:
        vids = set()
        c.execute('select vehicle_id from es8_delivery where activate_time <  %s and type=1',(dt))
        rs = c.fetchall()
        for r in rs:
            vids.add(r.get('vehicle_id'))
        return vids

def get_rate(new_set,active_set):
    if new_set == None or active_set == None or len(new_set) == 0:
        return 'N/A'
    return '{:.2%}'.format(float(len(new_set.intersection(active_set))) / len(new_set))

def detail_retention(year,month):
    p1 = get_month_before(year,month,1)
    mnu_1 = get_mnu_vids(p1[0],p1[1])

    p2 = get_month_before(year, month, 2)
    mnu_2 = get_mnu_vids(p2[0], p2[1])

    dr = get_month_date_range(p1[0], p1[1])
    mnu_old = get_new_vids_before(dr[0])
    print(dr[0]+' before vids')

    print(len(mnu_1))

    days = get_month_days(year,month)

    mnu_d = set()

    rr = {}
    for d in days:
        dt = datetime(year,month,d)

        dau = get_dau_vids(dt)

        # 累积计算当月新用户
        mnu_d = mnu_d.union(get_dnu_vids(dt))

        # 当月提车用户留存率
        r0 = get_rate(mnu_d,dau)

        # 上月提车用户月留存率
        r1 = get_rate(mnu_1, dau)

        # 上上月提车用户月留存率
        r2 = get_rate(mnu_2, dau)

        # 历史老用户
        ro = get_rate(mnu_old, dau)

        rr[dt.strftime('%Y-%m-%d')] = [r0,r1,r2,ro]
    m_key = get_month_key(year,month)
    ssdb_save('retention.detail.'+m_key, rr)

def gen_all_weekly_retention():
    dt = datetime.now()
    for i in range(0, 10):
        monday = dt - timedelta(days=(dt.weekday() + i * 7))
        weekly(monday)

def gen_all_monthly_retention():
    for i in range(7,10):
        monthly(2018, i)

def gen_all_daily_retention():
    for dt in get_all_days():
        daily(datetime.strptime(dt, "%Y-%m-%d"))

if __name__ == '__main__':
    init()
    #detail_retention(2018,10)
    #daily(datetime.strptime('2018-09-29', "%Y-%m-%d"))
    # gen_all_daily_retention()
    # gen_all_monthly_retention()
    # gen_all_weekly_retention()
    #retention_rate(datetime.strptime("2018-09-21", "%Y-%m-%d"))
    # http://sariel.nioint.com/api/ssdb/get?keys=
    #daily_retention('2018-09-21')
    monthly(2019,1)
    #today = date.today()
    #dt = datetime.strptime( "2012-10-09", "%Y-%m-%d")
    #dt = datetime.now()
    #monday = dt - timedelta(days=(dt.weekday()))

    #weekly(monday)
    #monthly(2018,9)