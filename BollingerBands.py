#This takes a symbol and finds Bollinger Band data to display on a graph

import pandas as pd
import matplotlib.pyplot as plt
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
df2 = pd.DataFrame()
df2['Distance'] = round(df['Real Upper Band'] - df['Real Lower Band'], 2)
df2.set_index(df.index)

dflist = [df, df2]
fig, ax = plt.subplots()
# Twin the x-axis twice to make independent y-axes.
axes = [ax, ax.twinx()]
# Make some space on the right side for the extra y-axis.
fig.subplots_adjust(right=0.75)
# Move the last y-axis spine over to the right by 10% of the width of the axes
axes[-1].spines['right'].set_position(('axes', 1.1))
# To make the border of the right-most axis visible, we need to turn the frame
# on. This hides the other plots, however, so we need to turn its fill off.
axes[-1].set_frame_on(True)
axes[-1].patch.set_visible(False)
# And finally we get to plot things...
"""
for i, ax in enumerate(axes):
    data = dflist[i-1]
    print(data)
    ax.plot(data)
    if i-1 == 0:
       ax.set_ylabel('Bollinger Band Values')
    elif i-1 == 1:
        ax.set_ylabel('Width of Span')
        print(max(data['Real Upper Band']))
        ax.set_ylim(top=max(df['Real Upper Band']))
    ax.tick_params(axis='y')
axes[0].set_xlabel('Dates, Bands calculated {}'.format(interval))
"""
df['Distance'] = df2['Distance']
"""
axes[0].plot(df)
axes[0].set_ylabel('Bollinger Band Values')
axes[0].tick_params(axis='y')
axes[1].plot(df2)
axes[1].set_ylabel('Distance')
typicalmax = max(df['Real Upper Band'])
axes[1].set_ylim(top=typicalmax, bottom=5, auto=False)
axes[1].tick_params(axis='y')
axes[0].set_xlabel('Dates (Bands calculated {})'.format(interval))
"""


plt.legend(df)
plt.figure(figsize=(12, 8))


plt.title('Calculated {} and based on {} time series points. '
          'Prices are prices at \'{}\''.format(interval, time_period, series_type),
          fontsize=20)
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
plt.show()