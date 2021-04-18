import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# must add this line in order for the app to be deployed successfully on Heroku
# from app import server
# from app import app
# from apps import shot_chart, def_hustle, home

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# search_bar = dbc.Row([
# 	dbc.Col([dbc.Input(id='search-bar', type='Search Player', placeholder='Search Player')]),
# 	dbc.Col([
# 		dbc.Button('Search', color='#3494F6', className='ml-2')
# 		], width='auto')

# ], no_gutters=True, className='ml-auto flex-nowrap mt-3 mt-md-0', align='center')

# nav_bar = dbc.Navbar([
# 			dbc.Col(html.Img(src='assets/yahoo_logo.png', height='40px')),
# 			dbc.NavLink("Home", href='/', active='exact'),
# 			dbc.NavLink("Player Stats & Analytics", href='/apps/player-stats', active='exact'),
# 			dbc.NavLink("Defensive Hustle Stats", href='/apps/def-hustle', active='exact')
# 	        ],
# 	        color='#3494F6',
# 	        sticky='top'
# 	    )

# PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search Player")),
        dbc.Col(
            dbc.Button("Search", color="success", className="ml-2"),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

nav_bar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src='assets/yahoo_logo.png', height="40px")),
                    dbc.NavLink("Home", href='/', active='exact'),
					dbc.NavLink("Player Stats & Analytics", href='/apps/player-stats', active='exact'),
					dbc.NavLink("Defensive Hustle Stats", href='/apps/def-hustle', active='exact')
                ],
                align="center",
                no_gutters=True,
            ),
            href="https://nba.com",
        ),
        # dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="#3494F6",
    # dark=True,
)
app.layout = html.Div([
	# dbc.Row([
	# 	dbc.Col(search_bar),
	# 	dbc.Col(nav_bar),
	# ]),
	# search_bar,
	nav_bar,
	html.Br(),
	html.P('random text', className='text-center')
	])


# app.layout = html.Div([
# 	# dbc.Row([
# 			dcc.Location(id='url'),
# 			dbc.Navbar(children=[
# 				# dbc.Row([
# 				# 	dbc.Col([html.Img(src='/assets/nba_logo.png', height='30px')]),
# 				# 	dbc.Col([dbc.NavbarBrand("NBA Analytics")])
# 				# ], align='center', no_gutters=True),
# 				dbc.NavLink("Home", href='/', active='exact'),
# 				dbc.NavLink("Player Stats & Analytics", href='/apps/player-stats', active='exact'),
# 				dbc.NavLink("Defensive Hustle Stats", href='/apps/def-hustle', active='exact')
# 		        ],
# 		        color='#3494F6',
# 		        sticky='top'
# 		    ),

#     html.Br(),
# 	dbc.Container(id='page-content', children=[])
# ])

# @app.callback(
# 	Output(component_id='page-content', component_property='children'),
# 	[Input(component_id='url', component_property='pathname')])
# def render_page_content(pathname):
# 	if pathname == '/':
# 		return home.layout
# 	elif pathname == '/apps/player-stats':
# 		return shot_chart.layout
# 	elif pathname == '/apps/def-hustle:':
# 		return def_hustle.layout

if __name__ == '__main__':
	app.run_server(port='4000',debug=True)