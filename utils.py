import pandas as pd
import heapq
import operator
import plotly.express as px
import plotly.graph_objects as go


_ohlc = ['open','high','low','close']
_ohlcv = _ohlc + ['volume']


def printlist(l, title=""):
    print(title)
    for x in l:
        print(x)
    

def filter_name_date(df, name, date=None):
    # filter names
    df = df.groupby("name").get_group(name).copy()

    # print available dates
    df['date'] = df['datetime'].dt.date
    available_dates = df['date'].unique()
    print("Available dates")
    for x in available_dates:
        print(str(x))

    # filter by date
    if date is not None:
        date = pd.to_datetime(date).date()
        if date not in available_dates:
            raise(Exception(f"{date} Date not in data"))

        df = df[df['date'] == date]
    return df


def showOHLC(df):
    fig = go.Figure(data=go.Candlestick(
                        x=df['datetime'],
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close']))
    fig.update_yaxes(fixedrange=False)
    # fig.show()
    return fig





def df_filter_times(df, start_time='9:30', end_time='15:59'):
    start_time = pd.to_datetime(start_time).time()
    end_time = pd.to_datetime(end_time).time()
    filtered_df = df[
        (df['datetime'].dt.time >= start_time) &
        (df['datetime'].dt.time <= end_time)
    ]
    filtered_df['date'] = filtered_df['datetime'].dt.date
    return filtered_df


class Position():
    def __init__(self, buyprice, buytime, sellby, minprice, fillprice=None, filltype=None):
        self.buyprice = buyprice
        self.buytime = buytime
        self.sellby = sellby
        self.minprice = minprice
        self.fillprice = fillprice
        self.filltype = filltype

    def __lt__(self, obj):
        return self.buytime < obj.buytime

    def __repr__(self):
        return f"Buy {self.buyprice}, Minsell {self.minprice}, Fill {self.fillprice} Buytime {self.buytime} Sellby {self.sellby}"


class Heap:
    def __init__(self, usekey=False):
        self.usekey = usekey
        self.heap = []

    def push(self, item, key=-1):
        if self.usekey:
            heapq.heappush(self.heap, (key, item))
        else:
            heapq.heappush(self.heap, item)

    def pop(self):
        if self.heap:
            x = heapq.heappop(self.heap)
            if self.usekey:
                return x[1]
            else:
                return x
        else:
            return None

    def peek(self):
        if self.heap:
            x = self.heap[0]
            if self.usekey:
                return x[1]
            else:
                return x
        else:
            return None

    def size(self):
        return len(self.heap)


def get_company_summary(df):
    def proc(x):
        return pd.DataFrame({
            "price_avg":[int(x['close'].mean())],
            "volume_avg":[int(x['volume'].mean())],
            "price_med":[int(x['close'].median())],
            "volume_med":[int(x['volume'].median())],

            })
    df = df.groupby("name").apply(proc)
    return df