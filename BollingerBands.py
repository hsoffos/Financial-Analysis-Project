#This takes a symbol and finds Bollinger Band data to display on a graph

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.legend
from cb91visuals import *

# Bollinger Bands are typically examined for 6-month narrowness; more narrow = more interesting

func = 'BBANDS'
symbol = 'IBM'
interval = 'weekly'
time_period = '60'
series_type = 'close'
api = 'KM2RBMGCOTIXETTD'
datatype = 'csv'

df = pd.read_csv('https://www.alphavantage.co/query?function={}&symbol={}&' \
                 'interval={}&time_period={}&series_type={}&apikey={}&' \
                 'datatype={}'.format(func, symbol, interval, time_period, series_type, api, datatype),
                 index_col='time')

df = df.iloc[:-1000, :]
df = df.iloc[::-1]
df.index = pd.to_datetime(list(df.index), format = '%Y-%m-%d %H:%M')
df['Distance'] = round(df['Real Upper Band'] - df['Real Lower Band'], 2)

plt.figure(figsize=(12, 8))


plt.title('Calculated {} and based on {} time series points. '
          'Prices are prices at \'{}\''.format(interval, time_period, series_type),
          fontsize=20, pad=20)
plt.suptitle('{} Bollinger Bands'.format(symbol),fontsize=30)
count = 0
for val, stamp in zip(df.values, list(df.index)):  # Adding text labels to graph
    if count % 20 == 0 or count == len(df.values)-1 \
            and not count == len(df.values)-6:  # Don't get too crowded at the end
        plt.text(stamp, val[1], val[1], size=12)
        plt.text(stamp, val[0], val[0], size=12)
        plt.text(stamp, val[2], val[2], size=12)
        plt.text(stamp, val[3], val[3], size=12)
    count += 1


plt.plot(df)
plt.legend(df)

plt.show()