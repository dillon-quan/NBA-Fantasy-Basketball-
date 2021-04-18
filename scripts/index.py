import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import shot_chart, def_hustle
#from app import server # need it to deploy it

# styling the sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


# padding for the page content
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

content = html.Div(id='page-content', children=[], style=CONTENT_STYLE)

sidebar = html.Div([
	dbc.Nav([
		dbc.NavLink("Home", href='/', active='exact'),
		dbc.NavLink("Player Stats & Analytics 1", href='/apps/player-stats', active='exact'),
		dbc.NavLink("Defensive Hustle Stats", href='/apps/def-hustle', active='exact')
	], pills=True, vertical=True)
], style=SIDEBAR_STYLE)

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	sidebar,
	html.Div(id='page-content', children=[]
		,style=CONTENT_STYLE)
	])

@app.callback(
	Output(component_id='page-content', component_property='children'),
	Input(component_id='url', component_property='url'))
def render_page_content(pathname):
	if pathname == '/':
		return html.Div([
			html.H1(children='Home Page Place Holder',
					className='text-center text-black-50')
		])
	elif pathname == '/apps/player-stats':
		return shot_chart.layout
	elif pathname == '/apps/def-hustle:':
		return def_hustle.layout

if __name__ == '__main__':
	app.run_serve(host='127.0.0.:8050', debug=True)