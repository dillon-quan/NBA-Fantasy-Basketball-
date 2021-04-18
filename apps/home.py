import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from app import app

layout = html.Div([
	dbc.Container([
		dbc.Row([
			dbc.Col([
				html.H3(children='Yahoo! Fantasy Basketball Player Insight', className='text-center')
				])
		]),
		html.Hr(),
		dbc.Row([
			dbc.Col([
				html.P("""Welcome! This application was built to help average yahoo fantasy basketball players (like us)
						improve their win rate by allowing players to make better decisions through in-depth information
						on players."""
				),
				html.P(""" Be Patient! Stay Tuned! More to come! """)

				])
		])
	])
])
