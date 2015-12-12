# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
 
# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math as m

#calculates Bollinger bands for a stock
def bollinger(sym, start, end, period):
 
    #get timestamps
    #ldt_timestamps = du.getNYSEdays(start-dt.timedelta(days=period*2), end, dt.timedelta(hours=16))
    ldt_timestamps = du.getNYSEdays(start, end, dt.timedelta(hours=16))
 
    #retrieve data
    dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, [sym], ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    #fill data
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)
 
    #actual closing prices
    df_close = d_data['close']
 
    #calculate rolling mean and standard deviation
    ts_mean = pd.rolling_mean(df_close, period)
    ts_std = pd.rolling_std(df_close, period)
 
    #upper and lower bollinger bands
    ts_upper = ts_mean + ts_std
    ts_lower = ts_mean - ts_std
 
    #bollinger value indicator
    ts_bol_val = (df_close - ts_mean) / ts_std
    print 'bol=',ts_bol_val
    #plot prices, mean and bands
    plt.clf()
    plt.plot(ldt_timestamps, df_close)
    plt.plot(ldt_timestamps, ts_mean)
    plt.plot(ldt_timestamps, ts_upper)
    plt.plot(ldt_timestamps, ts_lower)
    plt.xlabel('Date')
    plt.ylabel('Closing Prices')
    plt.savefig('BOLLINGERBANDS.pdf', format='pdf') 
    return ts_bol_val
 
if __name__ == '__main__':
 
    start = dt.datetime(2010,1,1)
    end = dt.datetime(2010,12,31)
    sym = 'GOOG'
    bollinger(sym, start, end, 20)
