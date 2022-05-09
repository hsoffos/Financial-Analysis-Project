from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import time
from datetime import timezone, datetime, timedelta, date
import numpy as np


def unix_time_millis(dt):
    """Convert datetime to unix timestamp"""
    return int(time.mktime(dt.timetuple()))


def unix_to_datetime(unix):
    """Convert unix timestamp to datetime"""
    return pd.to_datetime(unix, unit='s')


def get_marks(start, end, Nth=100):
    """Return the marks for labeling. Every Nth value is used"""
    result = {}
    for i, date in enumerate(daterange):
        if i % Nth == 1:  # Append value to dict
            result[unix_time_millis(date)] = str(date.strftime('%Y-%m-%d'))
    return result


# Round values, keep within x-axis extremes. x range slider controls would sometimes be
# out of bounds of the actual data in the chart. Use this method to make sure
# the values from the x-axis range slider never exceed the actual time range of available data.
min_timestamp = datetime.timestamp(datetime(2001,1,1))
max_timestamp = datetime.timestamp(datetime(2031,1,1))
min_timestamp_chart = min_timestamp  #+ chart_shift
max_timestamp_chart = max_timestamp  #+ chart_shift
def keep_in_x_axis_bounds(value):
    global min_timestamp
    global max_timestamp
    adjusted_value = 0
    # If the bar slider returns a value outside the established minimum and maximum range, round up or down
    if value > max_timestamp:
        adjusted_value = max_timestamp
    elif value < min_timestamp:
        adjusted_value = min_timestamp
    else:
        adjusted_value = value
    return adjusted_value


# Gets the ordinal index (zero based index) of the bar in the data frame at the given time
def get_row_index_of_time(current_datetime):
    #       print('getRowIndexOfTime function called with arguments ' + str(currentDateTime) )
    # Make data and dateformat object available in scope of function
    global df
    global dateformat
    # Round date to a day increment using rounding function since our bar time period is 1 day.
    # {5 minute increment, 5 min}
    print(type(current_datetime), "typing")
    rounded_date_time = pd.to_datetime(current_datetime).date()
    print(rounded_date_time)

    print('object type returned from roundToFiveMinutes function ' + str(rounded_date_time))
    # Format date as MySQL date string. Used to locate the bar date in the pandas data frame
    index_time_string = rounded_date_time.strftime(dateformat)
    print(index_time_string)
    ##    print('index string for time value ' + index_time_string)
    # Get the ordinal row of the bar with that MySQL time stamp by using numpy array where function on the time column.
    row_index = np.where(pd.to_datetime(df['time']) == index_time_string)[0]
    print('row index of date in csv file: ' + str(row_index))
    # The numpy 'where' function returns list of indexes of all matches so only return first item in list
    # (returns an integer corresponding to row number for the bar with the correct MySQL date)
    # Note that this is not very robust. There is no error handling here if a row is NOT found in the data
    # with that database. In my experience there are periodically times when the x slider is adjusted and
    # I get an error, but if I adjust the slider again, it usually runs the script and works fine.
    # A more robust solution would be to have a function that makes sure we locate a valid
    # record in the dataframe every time. If your data is very sparse this could be a problem.
    return row_index[0]


# Find max or min price of the bars in a date range.
# Default: max is set to true (find the max price).
# If set to false, the function returns the minimum price.
def find_price_extreme(start_time, end_time):
    #       print('findPriceExtreme function called with arguments ' + str(startTime) + ' and ' + str(endTime) )
    min_row_index = get_row_index_of_time(start_time)
    max_row_index = get_row_index_of_time(end_time)
    #       print('min_row_index : ' + str(min_row_index))
    #       print('max_row_index : ' + str(max_row_index))
    #       print('found data minRow: ' + str(df.iloc[min_row_index]))
    sl = slice(min_row_index, max_row_index + 1)
    #       print('slice object ' + str(sl))
    view_bar_data = df.iloc[sl]
    #       print(view_bar_data.head())
    #       print(view_bar_data.tail())
    # Example df.agg({'A' : ['sum', 'min'], 'B' : ['min', 'max']})
    max_bar_high = max(view_bar_data['high'])

    min_bar_low = min(view_bar_data['low'])
    #     print('max_bar_high : ' + str(max_bar_high))
    #     print('maxBarLow : ' + str(min_bar_low))
    return [min_bar_low, max_bar_high]

##create our list of data traces to be plotted on the chart. We will pass this to the plotly figure
##data = [firstTrace]
## create our layout and assign to a variable so we can updat the layout later.
##NOTES ON PARAMATERS:
##layout variable is created so we can access the x and y range values of our graph later in our dash callback functions.
##xaxis:range - set the min and max values on the x range of the chart to our minimum and maximum dates of the available data plus our offset of
##four hours which for some reason the graph always seems off by four hours. This was calculated above
##and assigned to the minTimeStampChart and maxTimeStampChart variables.
##yaxis:range - Also assign our min and max y range which is based on the max(high) and min(low) of all the bars in our available data to start with.
##the y min and max were calculated and stored in the newRangeLow and newRangeHigh variables already.
##autorange - make sure the ranges don't automatically scale since we are setting
##height - customize the height of our graph here. Dash defaults are too small to display bar data well.
##dtick - set the graph to show every price tick which in the bar data we are using is $.0001


utcTimeZone = timezone.utc
# INVESTIGATE BELOW
# I don't know why by on the plotly chart the range is
# always four hours off if the actual time stamps fed into the chart.
# The chartShift variable is used to make an adjustment to the time range each time
# the x range values are assigned to the chart to correct this. It does not seem to be a problem with the
# datetime objects or their conversion. It seems to be an issue were when you assign the x range values,
# the chart is four hours off. I don't know if plotly is somehow using a local time zone according
# to my computer system time, but it is odd that it is four hours off because I am on east coast time
# with a utc offset of -04:56 for my time zone compared to utc.
# This is four hours of seconds converted to microseconds (1 second/1000)
# chartShift = 14400 * 1000


app = Dash(__name__)  # Init Dash

df = yf.Ticker('IBM').history(period='1y')[map(str.title, ['open', 'close', 'low', 'high', 'volume'])]  # Yahoo Finance
df['symbol'] = 'IBM'  # For now, explicitly name symbol data

df.index = pd.to_datetime(list(df.index), format='%Y-%m-%d %H:%M')  #

df = df.reset_index()
df.columns = ['time', 'open', 'close', 'low', 'high', 'volume', 'symbol']
df.time = df.time.apply(lambda x: x.date())  # Drop time component, keep date
#print(df.tail())
daterange = df['time']  # Grab 'time' column
dateformat = '%Y-%m-%d %H:%M:%S'
tick_padding = .0002


# Get the price extremes for the bar data in the graph.
# In this case it is the first and last bar of our data. Use to set he yaxis starting values
date_min = min(df['time'])
date_max = max(df['time'])
#date_min = datetime.strptime(date_min, dateformat)
#date_max = datetime.strptime(date_max, dateformat)

starting_price_extreme = find_price_extreme(date_min, date_max)
new_range_low = round(starting_price_extreme[0], 4) - tick_padding
new_range_high = round(starting_price_extreme[1], 4) + tick_padding


layout = go.Layout(
    xaxis=dict(
        autorange=False,
        rangeslider=dict(
            visible=False
        ),
        type='date',
        range=[min_timestamp_chart, max_timestamp_chart]
    ),
    yaxis=dict(
        title='Ticks',
        titlefont=dict(
            family='Arial, sans-serif',
            size=18,
            color='lightgrey'
        ),
        showticklabels=True,
        tickangle=0,
        tickfont=dict(
            family='Old Standard TT, serif',
            size=14,
            color='black'
        ),
        exponentformat='e',
        showexponent='all',
        tickmode='linear',
        tick0=0.500,
        dtick=.0001,
        autorange=False,
        range=[new_range_low, new_range_high]

    ),
    height=800
)

app.layout = html.Div([  # Control the app's layout
    html.Div([

        html.Div([
            dcc.Dropdown(  # Dropdown for analytic functions
                ['BBANDS', 'MACD', 'RSI', 'CANDLES'],
                'CANDLES',
                id='func-name'
            ),
            dcc.RadioItems(  # Radio buttons, useful for these?
                ['Linear', 'Log'],
                'Linear',
                id='func-type',
                inline=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(  # Dropdown for ticker symbols
                df['symbol'].unique(),
                'IBM',
                id='yaxis-column'
            ),
            dcc.RadioItems(
                ['Linear', 'Log'],
                'Linear',
                id='yaxis-type',
                inline=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic'),

    dcc.RangeSlider(  # Slider for the graph
        # min=unix_time_millis(daterange.min()),  # Currently, adding min+max= AND value= result in bad slider format
        # max=unix_time_millis(daterange.max()),
        step=None,
        id='year--slider',
        value=[unix_time_millis(daterange.min()),
               unix_time_millis(daterange.max())],
        marks=get_marks(daterange.min(), daterange.max())
        # marks={str(year): str(year) for year in daterange.unique()},

    )
])


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('yaxis-column', 'value'),
    Input('yaxis-type', 'value'),
    Input('year--slider', 'value'))
def update_graph(yaxis_column_name, yaxis_type,
                 x_slider_value, xaxis_type=type(daterange[1]),
                 xaxis_column_name='time'):
    # fig = px.scatter(x=list(df['time']),
    #                  y=list(df['Open']))

    global data
    global layout
    global tick_padding

    fig = go.Figure(data=go.Candlestick(
        x=df['time'],
        open=df['open'],
        close=df['close'],
        low=df['low'],
        high=df['high']
    ))

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    fig.update_xaxes(title=xaxis_column_name,
                     type=xaxis_type if xaxis_type == 'Linear' else 'date')

    fig.update_yaxes(title=yaxis_column_name,
                     type='linear' if yaxis_type == 'Linear' else 'log')

    # Make data, layout, and y range padding values available in the scope of this function.


    # First calculate any change to the graph range based on x slider
    #       print('get range of xaxis' + str(layout['xaxis']['range']))
    print('values returned by x slider ' + str(x_slider_value))
    print(x_slider_value)
    # If the values returned by the slider exceed our allowed range adjust them.
    x_min_adjusted = keep_in_x_axis_bounds(x_slider_value[0])
    print("x adjusted min",x_min_adjusted)
    x_max_adjusted = keep_in_x_axis_bounds(x_slider_value[1])
    print("x adjusted max",x_max_adjusted)
    # print('x slider values corrected for out of bounds values [' + str(x_min_adjusted) + ','+ str(x_max_adjusted) + ']')

    xmin_date = unix_to_datetime(x_min_adjusted)
    xmax_date = unix_to_datetime(x_max_adjusted)
    print("min date", xmin_date)
    print("max date", xmax_date)
    #    print('x min date object ' + str(xmin_date))
    #    print('x max date object ' + str(xmax_date))
    xmin_chart_value = unix_time_millis(xmin_date)  # + chartShift
    xmax_chart_value = unix_time_millis(xmax_date)  # + chartShift
    #    print('setting xmin and xmax millesecond values on x range to : [' + str(xmin_chart_value) + ',' + str(xmax_chart_value) + ']')

    # Next calculate any change to the graph range based on y slider
    #    print('get range of yaxis' + str(layout['yaxis']['range']))
    # Find bars in date range
    new_y_range = find_price_extreme(xmin_date, xmax_date)
    new_range_low = round(new_y_range[0], 4) - tick_padding
    new_range_high = round(new_y_range[1], 4) + tick_padding
    ##    print('new range low and high for y axis ' + str(new_range_low) + ',' + str(new_range_high))
    layout['xaxis']['range'] = [xmin_chart_value, xmax_chart_value]
    layout['yaxis']['range'] = [new_range_low, new_range_high]

    # Now that we have updated our layout, assign it to our figure by returning thes values which reset the data and layout properties of the figure.
    # Note that this is why we made sure to create a reference to our layout. Another strategy could be to update your data and replot it, but here
    # we just update the layout, and pass back in the same data to the figure.
    return fig


#def adjust_ranges(x_slider_value):



if __name__ == '__main__':
    app.run_server(debug=True)
