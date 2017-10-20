# -*- coding: UTF-8 -*-

import datetime


######### http://my.oschina.net/u/234186/blog/61190 ###############

def get_tody():
    return datetime.date.today()




def get_current_week_fristday_lastday():

    date = get_tody()
    this_week_start_dt = date-datetime.timedelta(days=date.weekday())
    this_week_end_dt = date+datetime.timedelta(days=6-date.weekday())

    return this_week_start_dt,this_week_end_dt


def get_last_week_fristday_lastday():
    date = get_tody()
    last_week_start_dt = date-datetime.timedelta(days=date.weekday()+7)
    last_week_end_dt = date-datetime.timedelta(days=date.weekday()+1)

    return last_week_start_dt,last_week_end_dt



def get_current_month_fristday_lastday():

    date = get_tody()

    y=date.year
    m = date.month
    month_start_dt = datetime.date(y,m,1)

    if m == 12:

        month_end_dt = datetime.date(y+1,1,1) - datetime.timedelta(days=1)

    else:
        month_end_dt = datetime.date(y,m+1,1) - datetime.timedelta(days=1)

    return month_start_dt ,month_end_dt



def get_last_month_fristday_lastday():

    date = get_tody()

    y=date.year
    m = date.month

    if m==1:                    #如果是1月
        start_date=datetime.date(y-1,12,1)
    else:
        start_date=datetime.date(y,m-1,1)
    end_date=datetime.date(y,m,1) - datetime.timedelta(days=1)

    return  start_date,end_date