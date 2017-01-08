from dwapi import datawiz
from datetime import datetime, timedelta
import pandas as pd

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

def get_salary_data(dataframe):
    dataframe.sort_values(['date'], inplace=True)
    dataframe.set_index(['date'], inplace=True)

    num_columns = ['turnover', 'qty', 'receipts_qty', 'profit']
    grouped_sum = dataframe.groupby([dataframe.index])[num_columns].aggregate('sum')

    # transpose dataframe (swap rows with columns)
    df = grouped_sum.T

    # create difference dataframe
    df_diff = df.diff(axis=1)
    # create difference in % dataframe
    df_prc = df.T.pct_change().T.apply(lambda x: x * 100)
    # concat all dataframes together
    result = pd.concat([df, df_diff, df_prc], axis=1).T
    # reset index (current on dates) and sort by dates
    result.reset_index(inplace=True)
    result.sort_values(['date'], inplace=True)
    # set back index and transpose again
    result.set_index(['date'], inplace=True)

    # drop NaN columns (appeared after concat)
    result.dropna(inplace=True)
    # yet another rotation to make dates columns names again
    result = result.T

    # change columns names
    columns = []
    for num, col in enumerate(list(result.columns)[1:]):
        marker = num % 3
        if marker == 1:
            columns.append('(Diff) {0}'.format(col))
        elif marker == 2:
            columns.append('(Diff, %) {0}'.format(col))
        else:
            columns.append(col)
    columns.insert(0, result.columns[0])

    # applying change
    result.columns = columns

    s = result.to_html(classes='table', float_format=lambda x: "{0:.2f}".format(x))
    return s

def get_dynamic_data(dataframe):
    dataframe.sort_values(['date'], inplace=True)

    dataframe[['qty_change', 'profit_change']] = dataframe.groupby('name')[['qty', 'profit']].diff()

    increase = dataframe[dataframe.qty_change > 0][['name', 'qty_change', 'profit_change']]

    decrease = dataframe[dataframe.qty_change < 0][['name', 'qty_change', 'profit_change']]

    html_inc = increase.to_html(classes='table', float_format=lambda x: "{0:.2f}".format(x), index=False)
    html_dec = decrease.to_html(classes='table', float_format=lambda x: "{0:.2f}".format(x), index=False)

    return html_inc, html_dec