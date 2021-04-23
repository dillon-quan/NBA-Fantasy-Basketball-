import os
import re
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from draw_court import draw_plotly_court

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX],
				meta_tags=[{'name': 'viewport',
							'content': 'width=device-width, initial-scale=1.0'}]
	)

# data
DATA_DIR = os.getcwd()
df = pd.read_csv(os.path.join(DATA_DIR, 'data/shot_chart_data.csv'))
player_stats = pd.read_csv(os.path.join(DATA_DIR, 'data/player_career_data.csv'))

player_stats = player_stats.loc[:, ['PLAYER_NAME', 'SEASON_ID','TEAM_ABBREVIATION',
       'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A',
       'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL',
       'BLK', 'TOV', 'PF', 'PTS']]

#layout section
app.layout = html.Div([ 
	dbc.Container([
		dbc.Row([
			dbc.Col([
				html.H1(children='Player Stats & Analysis',
						className='text-center text-black-50')
			])
		], justify='start'),

		dbc.Row([
			dbc.Col([
				html.Div([
					html.H6(children='Select Player'),
					dcc.Dropdown(id='player-selection',
								 options=[{'label': i, 'value':i} for i in sorted(df.PLAYER_NAME.unique())],
								 value='Stephen Curry')
				])
			], width={'size':6, 'offset':0, 'order':1}),

			dbc.Col([
				html.Div([
					html.H6(children='Select Season'),
					dcc.Dropdown(id='season-selection',
								 options=[{'label':i, 'value': i} for i in sorted(df.season.unique())],
								 value='2018-19')
				])
			], width={'size':6, 'offset':0, 'order':2})
		], justify='start'),

		dbc.Row([
			dbc.Col([
				html.Div([
					html.Br(),
					html.H6(children='Player PerGame Season Stats'),
					dash_table.DataTable(id='player-stats',
										 columns=[{'name': i, 'id': i} for i in player_stats.columns])
				])
			])
		]),

		dbc.Row([
			dbc.Col([
					html.Div([
						html.Br(),
						html.H6(children='Top 5 Most Taken Shot'),
						dash_table.DataTable(id='most-taken-shot',
											 columns=[{'name': 'ACTION_TYPE', 'id': 'ACTION_TYPE'}, 
							 {'name': 'SHOT_ZONE_BASIC', 'id': 'SHOT_ZONE_BASIC'},
							 {'name': 'Number of Shots Taken', 'id': 'GAME_ID'}])
					])
			],  width={'size':5, 'offset':0, 'order':1}),

			dbc.Col([
				html.Div([
					html.Br(),
					html.H6(children='Top 5 Most Made Shot'),
					dash_table.DataTable(id='most-made-shot',
										 columns=[{'name': 'ACTION_TYPE', 'id': 'ACTION_TYPE'}, 
						 {'name': 'SHOT_ZONE_BASIC', 'id': 'SHOT_ZONE_BASIC'},
						 {'name': 'Number of Shots Made', 'id': 'GAME_ID'}])
				])
			], width={'size':5, 'offset':2, 'order':2})
		], align='center', no_gutters=False, justify='start'),

		dbc.Row([
			dbc.Col([
				html.Div([
				html.Br(),
				dcc.Graph(id='shot-chart', figure={})]),
			], width={'offset':4})
		])
	]),

])
# callback
@app.callback(
	Output(component_id='shot-chart', component_property='figure'),
	Input(component_id='player-selection', component_property='value'),
	Input(component_id='season-selection', component_property='value')
	)
def update_shot_chart_graph(player, season):
	missed_shot_trace = go.Scatter(
		x=df.loc[(df.SHOT_MADE_FLAG == 0) & (df.PLAYER_NAME == player) & (df.season == season)]['LOC_X'],
		y=df.loc[(df.SHOT_MADE_FLAG == 0) & (df.PLAYER_NAME == player) & (df.season == season)]['LOC_Y'],
		mode='markers',
		name='Miss',
		marker={'color':'red', 'size':5},
		text=df.loc[(df.SHOT_MADE_FLAG == 0) & (df.PLAYER_NAME == player) & (df.season == season)]['ACTION_TYPE'] + "<br>" +
			  df.loc[(df.SHOT_MADE_FLAG == 0) & (df.PLAYER_NAME == player) & (df.season == season)]['SHOT_ZONE_RANGE']
		)

	made_shot_trace = go.Scatter(
		x=df.loc[(df.SHOT_MADE_FLAG == 1) & (df.PLAYER_NAME == player) & (df.season == season)]['LOC_X'],
		y=df.loc[(df.SHOT_MADE_FLAG == 1) & (df.PLAYER_NAME == player) & (df.season == season)]['LOC_Y'],
		mode='markers',
		name='Made',
		marker={'color':'green', 'size':5},
		text=df.loc[(df.SHOT_MADE_FLAG == 1) & (df.PLAYER_NAME == player) & (df.season == season)]['ACTION_TYPE'] + "<br>" +
			  df.loc[(df.SHOT_MADE_FLAG == 1) & (df.PLAYER_NAME == player) & (df.season == season)]['SHOT_ZONE_RANGE']
		)
	layout = go.Layout(
		title=f'{player} Shot Chart {season}',
		showlegend=True,
		xaxis={'showgrid':False, 'range':[-300, 300]},
		yaxis={'showgrid':False, 'range':[-100, 500]},
		height=600,
		width=650
		)
	fig = go.Figure(data=[missed_shot_trace, made_shot_trace], layout=layout)
	draw_plotly_court(fig, 600, margins=5)
	fig.update_layout(margin={'l': 0, 'b': 0, 't': 30, 'r': 0})
	return fig

@app.callback(
	Output(component_id='player-stats', component_property='data'),
	Input(component_id='player-selection', component_property='value'),
	Input(component_id='season-selection', component_property='value')
	)
def generate_table(player, season):
	data = player_stats.loc[(player_stats.PLAYER_NAME == player) & (player_stats.SEASON_ID == season)]
	data['FG_PCT'] = pd.to_numeric(player_stats['FG_PCT']).round(3)
	data['FG3_PCT'] = pd.to_numeric(player_stats['FG3_PCT']).round(3)
	data['FT_PCT'] = pd.to_numeric(player_stats['FT_PCT']).round(3)
	return data.to_dict('records')


@app.callback(
	Output(component_id='most-taken-shot', component_property='data'),
	Input(component_id='player-selection', component_property='value'),
	Input(component_id='season-selection', component_property='value')
	)
def most_taken_shot_table(player, season):
	data = (df.loc[(df.PLAYER_NAME == player) & 
        (df.season == season)][['ACTION_TYPE', 'SHOT_ZONE_BASIC', 'GAME_ID']]
    .groupby(by=['ACTION_TYPE', 'SHOT_ZONE_BASIC']).count().sort_values(by='GAME_ID', ascending=False)
    .reset_index()
    .head()
	)
	return data.to_dict('records')

@app.callback(
	Output(component_id='most-made-shot', component_property='data'),
	Input(component_id='player-selection', component_property='value'),
	Input(component_id='season-selection', component_property='value')
	)
def most_made_shot_table(player, season):
	data = (df.loc[(df.PLAYER_NAME == player) & 
        (df.season == season) & df.SHOT_MADE_FLAG == 1][['ACTION_TYPE', 'SHOT_ZONE_BASIC', 'GAME_ID']]
    .groupby(by=['ACTION_TYPE', 'SHOT_ZONE_BASIC']).count().sort_values(by='GAME_ID', ascending=False)
    .reset_index()
    .head()
	)
	return data.to_dict('records')

if __name__ == '__main__':
	app.run_server(port='4000',debug=True)