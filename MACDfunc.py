# This is a MACD function
import mplfinance
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from cb91visuals import *
import matplotlib.dates as mpl_dates

# Bollinger Bands are typically examined for 6-month narrowness; more narrow = more interesting

func = 'MACD'
symbol = 'IBM'
interval = 'weekly'
series_type = 'close'
api = 'KM2RBMGCOTIXETTD'
datatype = 'csv'

df_av_macd = pd.read_csv('https://www.alphavantage.co/query?function={}&symbol={}&' \
                 'interval={}&series_type={}&apikey={}&' \
                 'datatype={}'.format(func, symbol, interval, series_type, api, datatype),
                         index_col='time')
func = 'BBANDS'
time_period = '60'
df_av_bb = pd.read_csv('https://www.alphavantage.co/query?function={}&symbol={}&' \
                 'interval={}&series_type={}&apikey={}&' \
                 'datatype={}&time_period={}'.format(func, symbol, interval, series_type, api, datatype, time_period),
                         index_col='time')
df_av_bb = df_av_bb.iloc[:-862,:]
df_av_bb = df_av_bb.iloc[::-1]
df_av_macd = df_av_macd.iloc[:-888,:]
df_av_macd = df_av_macd.iloc[::-1]
print(df_av_macd)
# Request historic pricing data via finance.yahoo.com API
df_yf = yf.Ticker('IBM').history(period='1y')[map(str.title, ['open', 'close', 'low', 'high', 'volume'])]
print(df_yf)
df_av_macd.index = pd.to_datetime(list(df_av_macd.index), format ='%Y-%m-%d %H:%M')
#plt.plot(df)
#plt.show()
ap0 = [#mplfinance.make_addplot(df_av_bb['Real Upper Band'], color = color_list[0], panel=1),
       #mplfinance.make_addplot(df_av_bb['Real Lower Band'], color= color_list[1], panel=1),
       mplfinance.make_addplot(df_av_macd['MACD_Signal'], color=color_list[2], panel=2),
       mplfinance.make_addplot(df_av_macd['MACD'], color=color_list[3], panel=2)]
mplfinance.plot(df_yf, type='candle', style='yahoo', volume=True, main_panel=1, volume_panel=0, addplot=ap0)

#fig, (ax1, ax2) = plt.subplots(2, 1)

#ax1.plot(df_yf)
#ax2.plot(df_av)
#plt.show()
