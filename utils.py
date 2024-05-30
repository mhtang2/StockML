import pandas as pd
import heapq
import operator


def df_filter_times(df, start_time='9:30', end_time='16:00'):
    start_time = pd.to_datetime(start_time).time()
    end_time = pd.to_datetime(end_time).time()
    filtered_df = df[
        (df['datetime'].dt.time >= start_time) &
        (df['datetime'].dt.time <= end_time)
    ]
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
