import copy
import numpy as np

import datetime as dt
import pandas as pd
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep

def getData(startTime, endTime, stockList):
    ldt_timestamps = du.getNYSEdays(startTime, endTime, dt.timedelta(hours=16))

    dataobj = da.DataAccess('Yahoo')
    symbols = dataobj.get_symbols_from_list(stockList)
    symbols.append('SPY')
    print(symbols)

    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    marketData = dict(zip(ls_keys, ldf_data))

    for s_key in ls_keys:
        marketData[s_key] = marketData[s_key].fillna(method='ffill')
        marketData[s_key] = marketData[s_key].fillna(method='bfill')
        marketData[s_key] = marketData[s_key].fillna(1.0)
    
    return symbols, marketData

def bollingerBand(marketData, lookbackPeriod):
    price = marketData['close']
    rolling_mean = pd.stats.moments.rolling_mean(price, lookbackPeriod)
    rolling_std = pd.stats.moments.rolling_std(price, lookbackPeriod)
    bollingerValue = (price - rolling_mean) / rolling_std
    return bollingerValue

def findEvent(symbols, bollingerValue, lookbackPeriod, t1, t2, t3):
    '''
    @param t1 threshold for bollinger value for the equity today
    @param t2 threshold for bollinger value for the equity yesterday
    @param t3 threshold for bollinger value for SPY today
    '''
    print "Finding Events"

    # Creating an empty dataframe
    events = copy.deepcopy(bollingerValue)
    events = events * np.NAN

    # Time stamps for the event range
    timestamps = bollingerValue.index

    totalEvent = 0
    for sym in symbols:
        for i in range(lookbackPeriod, len(timestamps)):
            bollingerToday = bollingerValue[sym].ix[timestamps[i]]
            bollingerYesterday = bollingerValue[sym].ix[timestamps[i-1]]
            bollingerSPYToday = bollingerValue['SPY'].ix[timestamps[i]]
            if bollingerToday <= t1 and bollingerYesterday >= t2 and bollingerSPYToday >= t3:                
                events[sym].ix[timestamps[i]] = 1
                totalEvent += 1

    return events, totalEvent


def main():
    startTime = dt.datetime(2008, 1, 1)
    endTime = dt.datetime(2009, 12, 31)
    lookbackPeriod = 20
    symbolList = 'SP5002012'
    t1, t2, t3 = -2.0, -2.0, 1.2
    symbols, marketData = getData(startTime, endTime, symbolList)
    bollingerValue = bollingerBand(marketData, lookbackPeriod)
    # print(bollingerValue)
    events, totalEvent = findEvent(symbols, bollingerValue, lookbackPeriod, t1, t2, t3)
    ep.eventprofiler(events, marketData, i_lookback=20, i_lookforward=20,
                s_filename=symbolList+'.pdf', b_market_neutral=True, b_errorbars=True,
                s_market_sym='SPY')
    print(totalEvent)


if __name__ == '__main__':
    main()