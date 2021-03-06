# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import operator
import sys
import csv

def fetchNYSEData(dt_start, dt_end, ls_symbols,period):

    # The Time of Closing is 1600 hrs
    dt_timeofday = dt.timedelta(hours=16)

    # Get a list of trading days between the start and the end.
    #ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)

    # Creating an object of the dataaccess class with Yahoo as the source.
    c_dataobj = da.DataAccess('Yahoo', cachestalltime=0)

    # Keys to be read from the data, it is good to read everything in one go.
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Reading the data, now d_data is a dictionary with the keys above.
    # Timestamps and symbols are the ones that were specified before.
    ldf_data = c_dataobj.get_data(ldt_timestamps, ls_symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))

    timestampsForNYSEDays = d_data['close'].index

    # Filling the data for NAN
    for s_key in ls_keys:
        d_data[s_key] = d_data[s_key].fillna(method='ffill')
        d_data[s_key] = d_data[s_key].fillna(method='bfill')
        d_data[s_key] = d_data[s_key].fillna(1.0)

    # Getting the numpy ndarray of close prices.
    na_price = d_data['close'].values

    # returning the closed prices for all the days
    return na_price, ldt_timestamps


def bollinger(df_closingPrices, lookbackPeriod):

    # Fetching the symbols from the dataframe column.
    ls_symbols = df_closingPrices.columns.values

    # an empty np_array with 0 columns and len(df_closingPrices) number of rows
    temp =np.zeros((len(df_closingPrices),0))

    # Creating three dataframes which will keep the moving_avg, moving_stddev and bollinger_vals
    df_movingavg = pd.DataFrame(temp, index =  df_closingPrices.index)
    df_movingstddev = pd.DataFrame(temp, index =  df_closingPrices.index)
    df_bollinger_vals = pd.DataFrame(temp, index =  df_closingPrices.index)

    # For all the symbols
    for symbol in ls_symbols:
        # Calculate the moving avg and assign it to the df_movingavg for that symbol
        df_movingavg[symbol] = pd.Series(pd.rolling_mean(df_closingPrices[symbol], lookbackPeriod), index= df_movingavg.index)

        # Calculate the moving stddev and assign it to the df_movingstddev for that symbol
        df_movingstddev[symbol] = pd.Series(pd.rolling_std(df_closingPrices[symbol], lookbackPeriod), index= df_movingstddev.index)

        # Calculate the bollinger values using 'Bollinger_val = (price - rolling_mean) / (rolling_std)'
        # and assign it to the df_bollinger_vals for that symbol
        df_bollinger_vals[symbol] = (df_closingPrices[symbol] - df_movingavg[symbol])/df_movingstddev[symbol]

    # returning the bollinger values, the sma and rolling stddev
    return df_bollinger_vals, df_movingavg, df_movingstddev


#draw Bollinger bands for a stock
def bollinger_graph(sym, start, end, period):

    #get timestamps
    #ldt_timestamps = du.getNYSEdays(start-dt.timedelta(days=period*2), end, dt.timedelta(hours=16))
    ldt_timestamps = du.getNYSEdays(start-dt.timedelta(days=period*2), end, dt.timedelta(hours=16))

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
    plt.savefig('BOLLINGERBANDS2010.pdf', format='pdf')
    return ts_bol_val

def main():
    print 'Argument List:', str(sys.argv)

    # List of Symbols
    ls_symbols = "AAPL","GOOG","IBM","MSFT"

    # start and end days
    #still need to look for other year data why it is not coming
    startdaysplit = 2010,1,1
    enddaysplit = 2010,12,31

    # converting into dt
    dt_start = dt.datetime(int(startdaysplit[0]),int(startdaysplit[1]), int(startdaysplit[2]), 16, 00, 00)
    dt_end = dt.datetime(int(enddaysplit[0]),int(enddaysplit[1]), int(enddaysplit[2]), 16, 00, 00)

    # lookback period
    lookbackPeriod = int(20)

    # Fetching the NYSE data
    closingPrices, ldt_timestamps = fetchNYSEData(dt_start, dt_end, ls_symbols,lookbackPeriod)

    # Converting the two outputs from NYSEDataFetch into one dataframe
    df_closingprices = pd.DataFrame(closingPrices, columns = ls_symbols, index = ldt_timestamps)

    # Sending the df_closingprices and lookback period to get the bollinger band values, simple moving average of the equities and rolling stddev of the equities
    df_bollinger_vals, df_movingavg, df_movingstddev = bollinger(df_closingprices, lookbackPeriod)

    print df_bollinger_vals.to_string()
    #provide single symbol
    bollinger_graph("GOOG", dt_start, dt_end, 20)

if __name__ == '__main__':
    main()
