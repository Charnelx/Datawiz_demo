from dwapi import datawiz
from datetime import datetime, timedelta

def api_conn(login, password):
    dw = datawiz.DW(login, password)
    return dw

def date_convertor(date_range):
    week = timedelta(weeks=1)
    month = timedelta(weeks=4)
    year = timedelta(weeks=48)

    period = None

    start_date, end_date = date_range.replace(' ', '').split('-')
    dt_start = datetime.strptime(start_date, '%d.%m.%Y')
    dt_end = datetime.strptime(end_date, '%d.%m.%Y')

    diff = dt_end - dt_start

    if diff < week:
        period = datawiz.DAYS
    elif diff < month * 2:
        period = datawiz.WEEKS
    elif diff < year:
        period = datawiz.MONTHS
    else:
        period = datawiz.YEARS

    conv_start = dt_start.strftime('%Y-%m-%d')
    conv_end = dt_end.strftime('%Y-%m-%d')

    return conv_start, conv_end, period



