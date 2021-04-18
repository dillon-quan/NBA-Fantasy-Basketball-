import os
import re
import pathlib
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from datetime import date
from collections import Counter

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from app import app


# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
df = pd.read_csv(DATA_PATH.joinpath('final_2021_schedule.csv'))
standing = pd.read_csv(DATA_PATH.joinpath('2021_standings.csv'))

layout = dbc.Container([
	dbc.Row([
		dbc.Col([
			html.H1(children='NBA 2021 Season Weekly Schedule',
					className='text-center'
			)
		])
	]),
	html.Hr(),
	html.Br(),
	dbc.Row([
		dbc.Col([
			dcc.Dropdown(id='week-dropdown',
						 options=[{'label': i, 'value': i} for i in df.week.unique()],
						 value=df.loc[(df.date == date.today().strftime('%m/%d/%Y')), 'week'].values[0]
						)
		], width={'size':3})
	]),
	html.Br(),
	dbc.Row([
		dbc.Col([
			dcc.Graph(id='game-count', figure={})
		], width={'size':6})
	])
])

@app.callback(
	Output(component_id='game-count', component_property='figure'),
	Input(component_id='week-dropdown', component_property='value')
	)
def update_graph(week):
	data = df.loc[df.week == week]
	visitor = Counter(data.loc[(data.week == week)].visitor.values)
	home = Counter(data.loc[(data.week == week)].home.values)
	game_count = home + visitor
	data = pd.DataFrame({'Team': list(game_count.keys()), 'n_games': list(game_count.values())})
	data = data.sort_values(by='Team')
	color_discrete_map={"Brooklyn Nets": '#000000', "Los Angeles Lakers": '#552781',"Cleveland Cavaliers": '#6F263D',
					"Indiana Pacers": '#F6BA33', "Orlando Magic": '#287DC5', "Philadelphia 76ers": '#1560BD',
					"Toronto Raptors": '#B52F25', 'Boston Celtics': '#55AA62', 'Chicago Bulls': '#D5392E',
					"Memphis Grizzlies": '#05274A', "Minnesota Timberwolves": '#236193', 'Denver Nuggets': '#F7C133',
					'Portland Trail Blazers': '#000000', 'Phoenix Suns': '#1F1861', 'Miami Heat': '#000000',
					'Milwaukee Bucks': '#2D5234', 'Charlotte Hornets': '#3B8DAA', 'Detroit Pistons': '#0C519A',
					'Washington Wizards': '#C73531', 'New York Knicks': '#EE8133', 'San Antonio Spurs': '#000000',
					'Utah Jazz': '#00275E', 'Sacramento Kings': '#393997', 'Los Angeles Clippers': '#D73932',
					'New Orleans Pelicans': '#0C2340', 'Golden State Warriors': '#0D529C', 'Atlanta Hawks':'#DD3C3D',
					'Dallas Mavericks': '#0157B8', 'Oklahoma City Thunder': '#297CC2', 'Houston Rockets': '#DA3A2F'}
	fig = px.bar(data, x='n_games', y='Team', orientation='h', color='Team', color_discrete_map=color_discrete_map)
	fig.update_layout(width=800, height=700, xaxis=dict(title_text='Number of Games', tickvals=[1, 2, 3, 4]), showlegend=False,
					plot_bgcolor='white', margin={'l': 0, 'b': 0, 't': 30, 'r': 0}, title='Weekly Total Games')
	return fig