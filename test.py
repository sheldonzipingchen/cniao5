# -*- coding: UTF-8 -*-

import sys
from urlparse import urlparse

from app.util.date_util import get_current_month_fristday_lastday, get_last_month_fristday_lastday

reload(sys)
sys.setdefaultencoding( "utf-8" )






if __name__ == "__main__":


    import datetime
    import time

    # today= datetime.datetime.strftime(datetime.datetime.today(), '%Y-%m-%d')
    # print today+" 00:00:00"
    # print today+" 23:59:59"

    month_start_dt,month_end_dt=get_last_month_fristday_lastday()



    print  month_start_dt
    print  month_end_dt









