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

# data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
df = pd.read_csv(DATA_PATH.joinpath('2021_schedule.csv'))

# Conference Standing data
standing = pd.read_csv(DATA_PATH.joinpath('2021_standings.csv'))
standing['W/L%'] = pd.to_numeric(standing['W/L%']).round(3)

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
	]),
	html.Br(),
	html.Br(),
	html.H4(children='NBA Season Standings'),
	html.Hr(),
	dbc.Row([
		dbc.Col([
			html.Div([
				html.H6(children='Eastern Conference Standings'),
				dash_table.DataTable(id='east-conf',
									 columns=[{'name': i, 'id': i} for i in standing.columns],
									 data=standing.loc[(standing.Conference == 'East')].to_dict('records'))
			])
		], width={'size':4, 'offset':0}),
		dbc.Col([
			html.Div([
				html.H6(children='Western Conference Standings'),
				dash_table.DataTable(id='west-conf',
									 columns=[{'name':i, 'id':i} for i in standing.columns],
									 data=standing.loc[(standing.Conference == 'West')].to_dict('records'))
			])
		], width={'size':4, 'offset':2})
	]),
	html.Br(),
	html.Br()
])


@app.callback(
	Output(component_id='game-count', component_property='figure'),
	Input(component_id='week-dropdown', component_property='value')
	)
def update_bargraph(week):
	data = df.loc[df.week == week]
	t1 = data[['visitor', 'home']]
	t2 = data[['home', 'visitor']].rename(columns={'home':'visitor', 'visitor':'home'})
	matchup = pd.concat([t1,t2])
	standing['Difficulty'] = standing['PS/G'] - standing['PA/G']
	merged = matchup.merge(standing[['Team', 'Difficulty']], left_on='home', right_on='Team', how='inner')
	merged = merged[['visitor', 'Team','Difficulty']].groupby(by='visitor').agg({'Team':'count', 'Difficulty':'mean'})
	merged['Number of Games'] = merged['Team'].astype('str')
	merged = merged.reset_index().sort_values('visitor', ascending=False)
	merged['Team'] = merged['visitor'].astype('category')
	fig = px.bar(merged, x='Difficulty', y='Team', orientation='h', color='Number of Games')
	fig.update_layout(width=800, height=700, xaxis=dict(title_text='Average Matchup Pts Score - Pts Allow'),
					plot_bgcolor='white', margin={'l': 0, 'b': 0, 't': 30, 'r': 0}, title='Weekly Team Matchups Difficulty')
	return fig