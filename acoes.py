
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
# import pandas_datareader.data as web
# import yfinance as yf
from datetime import datetime 
import yfinance as yf
import json
import urllib.request
# yf.pdr_override()



def get_data(name, period="1mo", interval="1d",
            start=None, end=None, prepost=False, actions=True,
            auto_adjust=True, back_adjust=False, repair=False, keepna=False,
            proxy=None, rounding=False, timeout=10,
            debug=True, raise_errors=False):
    """
    :Parameters:
        period : str
            Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            Either Use period parameter or use start and end
        interval : str
            Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
            Intraday data cannot extend last 60 days
        start: str
            Download start date string (YYYY-MM-DD) or _datetime, inclusive.
            Default is 1900-01-01
            E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
        end: str
            Download end date string (YYYY-MM-DD) or _datetime, exclusive.
            Default is now
            E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
        prepost : bool
            Include Pre and Post market data in results?
            Default is False
        auto_adjust: bool
            Adjust all OHLC automatically? Default is True
        back_adjust: bool
            Back-adjusted data to mimic true historical prices
        repair: bool or "silent"
            Detect currency unit 100x mixups and attempt repair.
            If True, fix & print summary. If "silent", just fix.
            Default is False
        keepna: bool
            Keep NaN rows returned by Yahoo?
            Default is False
        proxy: str
            Optional. Proxy server URL scheme. Default is None
        rounding: bool
            Round values to 2 decimal places?
            Optional. Default is False = precision suggested by Yahoo!
        timeout: None or float
            If not None stops waiting for a response after given number of
            seconds. (Can also be a fraction of a second e.g. 0.01)
            Default is 10 seconds.
        debug: bool
            If passed as False, will suppress
            error message printing to console.
        raise_errors: bool
            If True, then raise errors as
            exceptions instead of printing to console.
    """
    stock = yf.Ticker(name)
    data = stock.history(period=period, interval=interval,
            start=start, end=end, prepost=prepost, actions=actions,
            auto_adjust=auto_adjust, back_adjust=back_adjust, repair=repair, keepna=keepna,
            proxy=proxy, rounding=rounding, timeout=timeout,
            debug=debug, raise_errors=raise_errors)
    return data


def add_to_data(data, indicators, columns_names):
    try:
        for idx, indicator in enumerate(indicators):
            data[columns_names[idx]] = indicator
    except:
        return False
    return True


def SMA(data, period=30, column='Close'):
    '''simple moving average'''
    return data[column].rolling(window=period).mean()


def EMA(data, period=30, column='Close'):
    '''exponential moving average'''
    return data[column].ewm(span=period, adjust=False).mean()


def CMA(data, column='Close'):
    '''cumulative moving average'''
    return data[column].expanding().mean()


def MACD(data, period_long=26, period_short=12, period_signal=9):
    '''moving average convergence/divergence'''
    short_EMA = EMA(data, period=period_short)
    long_EMA = EMA(data, period=period_long)
    macd = short_EMA - long_EMA
    data['MACD'] = macd
    signal_line = EMA(data, period=period_signal, column='MACD')
    data.drop(['MACD'], axis=1, inplace=True)
    return macd, signal_line


def RSI(data, period=14, column='Close'):
    "relative strength index"
    delta = data[column].diff(1)
    delta = delta[1:]
    up = delta.copy()
    down = delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    data['up'] = up
    data['down'] = down
    avg_gain = SMA(data, period=period, column='up')
    avg_loss = abs(SMA(data, period=period, column='down'))
    rs = avg_gain/avg_loss
    
    data.drop(['up'], axis=1, inplace=True)        
    data.drop(['down'], axis=1, inplace=True)        
    return 100.0 - (100.0/(1.0 + rs))

    
def get_detailed_info(data):
    response = urllib.request.urlopen(f'https://query2.finance.yahoo.com/v1/finance/search?q={name}')
    content = response.read()
    return pd.DataFrame(json.loads(content.decode('utf8'))['quotes'])

    
def MF(data, period=14, column='Close'):
    """median filter"""
    return data.rolling(period, win_type='gaussian').mean(std=data.std().mean())


def ATR(data, period=14):
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    return true_range.rolling(period).sum()/period




if __name__ == "__main__":
    stock = get_data("PETR4.SA")
    print(len(stock.index))
    print("macd", len(RSI(stock).index))
