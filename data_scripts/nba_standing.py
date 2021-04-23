import os
import pathlib
import pandas as pd

def conference_seed_extract(val):
    return val.split()[-1].strip('()')
def remove_seed(val):
    return ' '.join(val.split()[:-1])

# get data
url = 'https://www.basketball-reference.com/leagues/NBA_2021_standings.html'
tables = pd.read_html(url)
east = tables[0]
east.rename(columns={'Eastern Conference': 'Team'}, inplace=True)
east['Conference'] = 'East'
west = tables[1]
west.rename(columns={'Western Conference': 'Team'}, inplace=True)
west['Conference'] = 'West'

# data preprocessing
standing = pd.concat([tables[0], tables[1]])
standing['Rank'] = standing['Team'].apply(conference_seed_extract)
standing['Team'] = standing['Team'].apply(remove_seed)

# writing to file
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
standing.to_csv(DATA_PATH.joinpath('2021_standings.csv'), index=False)