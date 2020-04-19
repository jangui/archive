import datetime as dt
import matplotlib.pyplot as plt
from matplotlib.pyplot import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

def get_data(symbol, output_filename, data_source):
    start = dt.datetime(2015,1,1)
    end = dt.datetime.now()

    df = web.DataReader(symbol, data_source, start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)
    #print(df.head())
    df.to_csv(output_filename)

#get_data('TSLA', 'tsla.csv', 'yahoo')

def load_data(filename):
    df = pd.read_csv(filename, parse_dates = True, index_col = 0)
    return df
    #df.head()

def plot(df):
    df.plot()
    plt.show()

def plot_better(df):
    from pandas.plotting import register_matplotlib_converters
    register_matplotlib_converters()

    ax1 = plt.subplot2grid((6,1),(0,0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6,1),(5,0), rowspan=5, colspan=1, sharex=ax1)

    ax1.plot(df.index, df['Adj Close'])
    ax1.plot(df.index, df['100ma'])
    ax2.plot(df.index, df['Volume'])
    plt.show()

def add_moving_average(df, days):
    df[str(days) + 'ma'] = df['Adj Close'].rolling(window=days, min_periods=0).mean()
    return df

def resample_data(df, days):
    df_ohlc = df['Adj Close'].resample(str(days) + 'D').ohlc()
    df_volume = df['Volume'].resample(str(days) + 'D').sum()
    return df_ohlc, df_volume

df = load_data('tsla.csv')
df = add_moving_average(df, 100)
plot_better(df)

