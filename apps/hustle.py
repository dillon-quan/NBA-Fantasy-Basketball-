import os
import re
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pathlib

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app import app

#data 
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
player_stats = pd.read_csv(DATA_PATH.joinpath("player_stats_2021.csv"))

cols = ['PLAYER_ID', 'PLAYER_POSITION', 'GP',
       'PTS', 'REB', 'AST', 'BLK', 'STL', 'TOV', 'FG3M', 'FGA', 'FG_PCT',
       'FTA', 'FT_PCT']

hustle = pd.read_csv(DATA_PATH.joinpath("hustle_player_stats_2021.csv"))

df = pd.merge(hustle, player_stats[cols], on='PLAYER_ID', how='inner')

contest_blk_fig = px.scatter(df, x='BLK', y='CONTESTED_SHOTS', 
                 hover_data=['PLAYER_NAME', 'MIN', 'CONTESTED_SHOTS_2PT', 'CONTESTED_SHOTS_3PT'],
                 color='PLAYER_POSITION')
contest_blk_fig.update_layout(paper_bgcolor='white', plot_bgcolor='white', title='Contested Shots vs Blocks')


deflect_blk_fig = px.scatter(df, x='BLK', y='DEFLECTIONS', 
                 hover_data=['PLAYER_NAME', 'MIN'],
                 color='PLAYER_POSITION')
deflect_blk_fig.update_layout(paper_bgcolor='white', plot_bgcolor='white', title='Deflections vs Blocks')


deflect_steal_fig = px.scatter(df, x='STL', y='DEFLECTIONS', 
                 hover_data=['PLAYER_NAME', 'MIN'],
                 color='PLAYER_POSITION')
deflect_steal_fig.update_layout(paper_bgcolor='white', plot_bgcolor='white', title='Deflections vs Steals')

contest_steal_fig = px.scatter(df, x='STL', y='CONTESTED_SHOTS', 
                 hover_data=['PLAYER_NAME', 'MIN','CONTESTED_SHOTS_2PT', 'CONTESTED_SHOTS_3PT'],
                 color='PLAYER_POSITION')
contest_steal_fig.update_layout(paper_bgcolor='white', plot_bgcolor='white', title='Contested Shots vs Steals')

layout = dbc.Container([
			dbc.Row([
				dbc.Col([
					html.H1(children='Hustle to Stats', className='text-center')
				])
			]),
			html.Hr(),
			dbc.Row([
				dbc.Col([
					dcc.Graph(id='contest-blk', figure=contest_blk_fig)
				], width={'size':5}),
				dbc.Col([
					dcc.Graph(id='deflect-blk', figure=deflect_blk_fig)
				], width={'size':5, 'offset':2})
			], no_gutters=False, align='center', justify='start'),
			html.Br(),
			dbc.Row([
				dbc.Col([
					dcc.Graph(id='contest-blk', figure=contest_steal_fig)
				], width={'size':5}),
				dbc.Col([
					dcc.Graph(id='deflect-blk', figure=deflect_steal_fig)
				], width={'size':5, 'offset':2})
			], no_gutters=False, align='center', justify='start'),
			# dbc.Row([
			# 	dbc.Col([html.H6("Random Text", className='text-center')])
			# ])
])