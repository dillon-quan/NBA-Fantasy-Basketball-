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
import numpy as np
from app import app

# data
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
df = pd.read_csv(DATA_PATH.joinpath('shot_chart_data.csv'))
player_stats = pd.read_csv(DATA_PATH.joinpath('player_career_data.csv'))

player_stats = player_stats.loc[:, ['PLAYER_NAME', 'SEASON_ID','TEAM_ABBREVIATION',
       'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A',
       'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL',
       'BLK', 'TOV', 'PF', 'PTS']]


# #layout section
layout = dbc.Container([
	dbc.Row([
		dbc.Col([
			html.H1(children='Player Stats & Analysis',
					className='text-center')
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
])

def draw_plotly_court(fig, fig_width=600, margins=10):        
    # From: https://community.plot.ly/t/arc-shape-with-path/7205/5
    def ellipse_arc(x_center=0.0, y_center=0.0, a=10.5, b=10.5, start_angle=0.0, end_angle=2 * np.pi, N=200, closed=False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a * np.cos(t)
        y = y_center + b * np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

    fig_height = fig_width * (470 + 2 * margins) / (500 + 2 * margins)
    fig.update_layout(width=fig_width, height=fig_height)

    # Set axes ranges
    fig.update_xaxes(range=[-250 - margins, 250 + margins])
    fig.update_yaxes(range=[-52.5 - margins, 417.5 + margins])

    threept_break_y = 89.47765084
    three_line_col = "#777777"
    main_line_col = "#777777"

    fig.update_layout(
        # Line Horizontal
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        yaxis=dict(
            scaleanchor="x",
            scaleratio=1,
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            ticks='',
            showticklabels=False,
            fixedrange=True,
        ),
        shapes=[
            dict(
                type="rect", x0=-250, y0=-52.5, x1=250, y1=417.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=-80, y0=-52.5, x1=80, y1=137.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="rect", x0=-60, y0=-52.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                # fillcolor='#333333',
                layer='below'
            ),
            dict(
                type="circle", x0=-60, y0=77.5, x1=60, y1=197.5, xref="x", yref="y",
                line=dict(color=main_line_col, width=1),
                # fillcolor='#dddddd',
                layer='below'
            ),
            dict(
                type="line", x0=-60, y0=137.5, x1=60, y1=137.5,
                line=dict(color=main_line_col, width=1),
                layer='below'
            ),

            dict(
                type="rect", x0=-2, y0=-7.25, x1=2, y1=-12.5,
                line=dict(color="#ec7607", width=1),
                fillcolor='#ec7607',
            ),
            dict(
                type="circle", x0=-7.5, y0=-7.5, x1=7.5, y1=7.5, xref="x", yref="y",
                line=dict(color="#ec7607", width=1),
            ),
            dict(
                type="line", x0=-30, y0=-12.5, x1=30, y1=-12.5,
                line=dict(color="#ec7607", width=1),
            ),

            dict(type="path",
                 path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(type="path",
                 path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
                 line=dict(color=main_line_col, width=1), layer='below'),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-220, y0=-52.5, x1=-220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=220, y0=-52.5, x1=220, y1=threept_break_y,
                line=dict(color=three_line_col, width=1), layer='below'
            ),

            dict(
                type="line", x0=-250, y0=227.5, x1=-220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=250, y0=227.5, x1=220, y1=227.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=17.5, x1=-80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=27.5, x1=-80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=57.5, x1=-80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=-90, y0=87.5, x1=-80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=17.5, x1=80, y1=17.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=27.5, x1=80, y1=27.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=57.5, x1=80, y1=57.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),
            dict(
                type="line", x0=90, y0=87.5, x1=80, y1=87.5,
                line=dict(color=main_line_col, width=1), layer='below'
            ),

            dict(type="path",
                 path=ellipse_arc(y_center=417.5, a=60, b=60, start_angle=-0, end_angle=-np.pi),
                 line=dict(color=main_line_col, width=1), layer='below'),

        ]
    )
    return True
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
