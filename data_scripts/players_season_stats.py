import os
import re
import pathlib
import pandas as pd
from nba_api.stats.static import teams
from nba_api.stats.endpoints import fantasywidget

# player data
fantasy = fantasywidget.FantasyWidget()
df_player = fantasy.get_data_frames()[0]

# team data
df_team = pd.DataFrame(teams.get_teams())
df_team.rename(columns={'id': 'team_id'}, inplace=True)

# merged (player & team)
data = df_player.merge(df_team[['abbreviation', 'full_name']], left_on='TEAM_ABBREVIATION', right_on='abbreviation', how='inner')
data.rename(columns={'full_name': 'TEAM_NAME'}, inplace=True)

# writing data to file
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
data.to_csv(DATA_PATH.joinpath(DATA_PATH, 'player_stats.csv'), index=False)