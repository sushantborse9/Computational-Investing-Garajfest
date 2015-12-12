#In this project you will create a basic market simulator that accepts
#trading orders and keeps track of a portfolio's value and saves it to a file.
#You will also create another program that assesses the performance of that
#portfolio.

# Import system libs
import csv
import math
import copy
import os
import sys
import pprint as pp
import time

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da
import QSTK.qstkstudy.EventProfiler as ep


helpMsg = """
    Market Simulator
    Execute as: python marketsim.py /s 1000000 orders.csv
                python marketsim.py /a 1000000 values.csv
    where 1000000 is the starting cash for the portfolio
    orders.csv is the orders file in form of year,mo,day,sym,[BUY|SELL],#shares
    2008, 12, 3, AAPL, BUY, 130
    2008, 12, 8, AAPL, SELL, 130
    2008, 12, 5, IBM, BUY, 50
    values.csv will be as below
    2008, 12, 3, 1000000
    2008, 12, 4, 1000010
    2008, 12, 5, 1000250
"""

def find_events(syms, data):
    """
    Generate the matrix with events
    syms : symbols
    data : data frame contaning values for different markers (open, close)
    Returns
    """
    data_close = data['actual_close']
    market = data_close['SPY']

    print "Finding events"

    # Create empty data frame
    events = copy.deepcopy(data_close)
    events = events * np.NAN

    # Time stamps for the event range
    timestamps = data_close.index

    for s in syms:
        for i in range(1, len(timestamps)):
            # Mark when price drops
            prev = data_close[s].ix[timestamps[i-1]]
            current = data_close[s].ix[timestamps[i]]
            dropped = prev >= 7.0 and current < 7.0
#            dropped = prev >= 5.0 and current < 5.0
            if dropped:
                events[s].ix[timestamps[i]] = 1

    return events

def frontier(startDate, endDate, symbol_filename, outfile) :
    # Get list of trading days between start and end date at the closing time.
    timeofday = dt.timedelta(hours=16)
    timeStamps = du.getNYSEdays(startDate, endDate, timeofday)

    # Keys to be read from the data, it is good to read everything in one go.
    keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']

    # Create access object and read all the data
    dataSrc = da.DataAccess('Yahoo')    # Read from Yahoo
    symbols = dataSrc.get_symbols_from_list(symbol_filename) # 'sp5002012')
    symbols.append('SPY')

    data = dataSrc.get_data(timeStamps, symbols, keys)
    sym_data = dict(zip(keys, data))

    # Replace NaN values with 1 and clear column if symbol was not found
    for key in keys:
        sym_data[key] = sym_data[key].fillna(method='ffill')
        sym_data[key] = sym_data[key].fillna(method='bfill')
        sym_data[key] = sym_data[key].fillna(1.0)

    t1 = time.time()
    events = find_events(symbols, sym_data)
    t2 = time.time()
    t = t2 - t1
    print " Time to find events: " + str(t) + " sec "

    profile = True

    if profile:
        print "Creating and Saving study as " + outfile
        t1 = time.time();
        ep.eventprofiler(events, sym_data, s_filename=outfile)
        t2 = time.time()
        t = t2 - t1
        print " Event profile took: " + str(t) + " sec "

def analyze(valuesFile, symbol):
    print " loading file... ", valuesFile
#    df = pd.read_csv(valuesFile, header=None, infer_datetime_format=True,
#                     parse_dates=True, keep_date_col=False)
#    print df.header
#    print df
    # load file
    timeStamps = []
    values = []
    delta = dt.timedelta(hours=16)
    try:
        reader = csv.reader(open(valuesFile, 'rU'), delimiter=',')
        for row in reader:
            y,m,d,v = row
            date = dt.datetime(int(y),int(m),int(d)) + delta
            timeStamps.append(date)
            values.append(float(v))
    except csv.Error as e:
            print "CSV writer error, file name: ", valuesFile, e

    tf = pd.TimeSeries(data=values, index=timeStamps)
    showplot = False
    if showplot:
        plot = tf.plot()
        fig = plot.get_figure()
        print "Analyze: save plot of daily return"
        fig.savefig("values.png")

    mean = tf.mean()
    norm_prices = tf.values / tf.values[0]
    print norm_prices

    cumulative_return = norm_prices[-1] # tf.values[-1]
    daily_returns = tsu.returnize0(norm_prices) # tf.values)
    avg_daily_return = np.average(daily_returns)
    sd = np.std(daily_returns)
    days = 252 # len(tf.values)
    sharpe_ratio = (math.sqrt(days) * np.mean(daily_returns)) / sd
    print "=================================================="
    print " Standard deviation:     ", sd
    print " Average daily return:   ", avg_daily_return
    print " Sharpe Ratio:           ", sharpe_ratio
    print " Cumulative return:      ", cumulative_return
    print "=================================================="

    # Get list of trading days between start and end date at the closing time.
    stDate = timeStamps[0]
    endDate = timeStamps[-1]
    print stDate, endDate
    timeStamps = du.getNYSEdays(stDate, endDate, dt.timedelta(hours=16))

    print "=================================================="
    print "================= " + symbol + " ========================="
    print "=================================================="
    # Keys to be read from the data, it is good to read everything in one go.
    keys = ['close'] # 'actual_close'] #
    syms = [symbol]

    # Create access object and read all the data
    dataSrc = da.DataAccess('Yahoo')    # Read from Yahoo
    data = dataSrc.get_data(timeStamps, syms, keys)
    sym_data = dict(zip(keys, data))

    # Replace NaN values with 1 and clear column if symbol was not found
    for key in keys:
        sym_data[key] = sym_data[key].fillna(method='ffill')
        sym_data[key] = sym_data[key].fillna(method='bfill')
        sym_data[key] = sym_data[key].fillna(1.0)

    norm_prices = sym_data['close'].values / sym_data['close'].values[0]
    cumulative_return = norm_prices[-1]
    daily_returns = tsu.returnize0(norm_prices)
    avg_daily_return = np.average(daily_returns)
    sd = np.std(daily_returns)
    days = 252 # len(tf.values)
    sharpe_ratio = (math.sqrt(days) * np.mean(daily_returns)) / sd
    print " Standard deviation:     ", sd
    print " Average daily return:   ", avg_daily_return
    print " Sharpe Ratio:           ", sharpe_ratio
    print " Cumulative return:      ", cumulative_return


def simulate(inFile, cash):
    print "Start parsing " + inFile
    orders_array = np.genfromtxt(inFile, dtype = None,
                                 names = ['Year', 'Month', 'Day', 'Symbol', 'Type', 'Amount', 'X'],
                                 delimiter = ',')
    orders_sorted = np.sort(orders_array, order=['Year', 'Month', 'Day'])

    row_0 = orders_sorted[0]
    row_n = orders_sorted[-1]
    stDate = dt.datetime(row_0[0], row_0[1], row_0[2])
    endDate = dt.datetime(row_n[0], row_n[1], row_n[2]) + dt.timedelta(days=1)
    unique_syms = np.unique(orders_array['Symbol']).tolist()

    print " Date Range: ", stDate, " to ", endDate
#    print unique_syms

    # Get list of trading days between start and end date at the closing time.
    timeofday = dt.timedelta(hours=16)
    timeStamps = du.getNYSEdays(stDate, endDate, timeofday)

    # Keys to be read from the data, it is good to read everything in one go.
    keys = ['open', 'close', 'actual_close'] #

    # Create access object and read all the data
    dataSrc = da.DataAccess('Yahoo')    # Read from Yahoo

    data = dataSrc.get_data(timeStamps, unique_syms, keys)
    sym_data = dict(zip(keys, data))

    # Replace NaN values with 1 and clear column if symbol was not found
    for key in keys:
        sym_data[key] = sym_data[key].fillna(method='ffill')
        sym_data[key] = sym_data[key].fillna(method='bfill')
        sym_data[key] = sym_data[key].fillna(1.0)

    # Create trade matrix
    trades = pd.DataFrame(data=0, index=timeStamps, columns=unique_syms)

    # Fill in trade matrix
    for order in orders_sorted:
        # Change date to closing time
        date = dt.datetime(order[0], order[1], order[2]) + dt.timedelta(hours=16)
        quantity = int(order['Amount'])
        if order['Type'] == 'Sell':
            quantity *= -1
        sym = order['Symbol']
        current = trades.get_value(date, sym)   # Same day trades
        trades.set_value(date, sym, current + quantity)

    transactions = trades.values * sym_data['close'].values
    total_transactions = transactions.sum(axis=1)    # map(sum, daily_portfolio)

    daily_cash_balance = pd.TimeSeries(cash, timeStamps)
    daily_cash_balance[0] -= total_transactions[0]
    for i in range(1,len(daily_cash_balance)):
        daily_cash_balance[i] = daily_cash_balance[i-1] - total_transactions[i]
#    print "Daily cash"
#    print daily_cash_balance

    # Propage holding over range so that we can computate holdings
    for i in range(1,len(trades.values)):
        trades.values[i] += trades.values[i-1]
    daily_portfolio = trades.values * sym_data['close'].values
    daily_holdings = daily_portfolio.sum(axis=1)    # map(sum, daily_portfolio)

    daily_total_portfolio = pd.TimeSeries(0, timeStamps)
    for i in range(len(daily_portfolio)):
        daily_total_portfolio[i] = daily_cash_balance[i] + daily_holdings[i]
#    print "Total worth "
#    print daily_total_portfolio

    savefig = False
    if savefig:
        plot = daily_total_portfolio.plot()
        fig = plot.get_figure()
        fig.savefig("./daily_total_portfolio.png")

    savecsv = True
    if savecsv:
        daily_total_portfolio.to_csv("./daily_total_portfolio.csv")

    savecsv_split = True
    if savecsv_split:
        try:
            fname = "values.csv"
            writer = csv.writer(open(fname, 'wb'), delimiter=',')
            #row = ['Date', 'Data']
            #writer.writerow(row)
            for r in daily_total_portfolio.index:
                dtime = r.to_datetime()
                value = daily_total_portfolio[r]
                #print dtime, type(dtime), value
                row = [dtime.year, dtime.month, dtime.day, value]
                writer.writerow(row)
        except csv.Error as e:
            print "CSV writer error, file name: ", fname, e

#    print daily_portfolio

if __name__ == "__main__":

        option = "a"
        startingCash = int('1000000')
        filename = "values.csv"
        if not os.path.isfile(filename):
            print " Failed to open : " + filename
        else:
            if option == 's':
                print "Start simulation...."
                # Parse input file and create md array
                orders = simulate(filename, startingCash)
            elif option == 'a':
                print "Start analysis with SPY ...."
                analyze(filename, '$SPX')
