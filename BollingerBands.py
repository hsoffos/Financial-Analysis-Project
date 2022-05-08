import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
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
print(df)

df.plot()
plt.show()
