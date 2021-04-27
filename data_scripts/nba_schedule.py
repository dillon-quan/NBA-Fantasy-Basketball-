# does not need to be refreshed daily

import re
import os
import pathlib
import pandas as pd
from datetime import datetime
from tqdm import tqdm


def remove_dow(val):
    return ','.join(val.split(',')[1:])

def dow_extract(val):
    return val.split(',')[0]

def mdy_to_ymd(d):
    return datetime.strptime(d, '%b %d, %Y').strftime('%m/%d/%Y')

# get data
data = pd.DataFrame()
for month in tqdm(['december', 'january', 'february', 'march', 'april', 'may']):
    url = f'https://www.basketball-reference.com/leagues/NBA_2021_games-{month}.html'
    df = pd.read_html(url)[0]
    df.columns = [col.lower() for col in df.columns]
    drop_cols = [col for col in list(df.columns) if re.search('unnamed|\s', col.lower())]
    drop_cols += ['notes', 'attend.']
    df = df.drop(columns=drop_cols)
    df.rename(columns={'visitor/neutral':'visitor', 'home/neutral':'home', 'pts':'vistor_pts', 'pts.1':'home_pts'}, inplace=True)
    df['dow'] = df.date.apply(dow_extract)
    df['date'] = df.date.apply(remove_dow)
    df['date'] = df.date.str.lstrip()
    df['date'] = df.date.apply(mdy_to_ymd)
    data = pd.concat([data, df])
  
# adding week column to schedule data  
temp = data[['dow', 'date']].loc[(data['dow'] == 'Sun')].drop_duplicates().reset_index()
for idx, _ in temp.iterrows():
    temp.loc[idx, 'week'] = f'Week {idx+1}'
data = data.merge(temp[['date', 'week']], on='date', how='left')
data['week'] = data.week.fillna(method='bfill')

# writing to file
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
data.to_csv(DATA_PATH.joinpath('2021_schedule.csv'), index=False)