import pandas as pd


def df_filter_times(df, start_time='9:30', end_time='16:00'):
    start_time = pd.to_datetime(start_time).time()
    end_time = pd.to_datetime(end_time).time()
    filtered_df = df[
        (df['datetime'].dt.time >= start_time) &
        (df['datetime'].dt.time <= end_time)
    ]
    return filtered_df
