import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# must add this line in order for the app to be deployed successfully on Heroku
from app import server
from app import app
from apps import shot_chart, hustle, home, schedule

app.layout = html.Div([
	dcc.Location(id='url'),
	dbc.Navbar(children=[
		dbc.Row([
			dbc.Col([html.Img(src='assets/yahoo_logo.png', height='30px')]),
			dbc.NavLink("Home", href='/', active='exact'),
			dbc.NavLink("Weekly Schedule", href='/apps/schedule', active='exact'),
			dbc.NavLink("Player Stats & Analytics", href='/apps/player-stats', active='exact'),
			dbc.NavLink("Defensive Hustle Stats", href='/apps/hustle', active='exact'),
        ])
        ],		        
        color='#3494F6',
        sticky='top'),
    html.Br(),
	dbc.Container(id='page-content', children=[])
])

@app.callback(
	Output(component_id='page-content', component_property='children'),
	[Input(component_id='url', component_property='pathname')])
def render_page_content(pathname):
	if pathname == '/':
		return home.layout
	elif pathname == '/apps/schedule':
		return schedule.layout
	elif pathname == '/apps/player-stats':
		return shot_chart.layout
	elif pathname == '/apps/hustle':
		return hustle.layout

if __name__ == '__main__':
	app.run_server(debug=True)