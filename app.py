# Essentail libraries
import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

# Import the dataset from "data" file
from data import *

# Import graphs from views
from graphs.borough_neighbourhood_count import *
from graphs.map import *
from graphs.room_types import *
from graphs.minimum_nights import *
from graphs.cancellation_policy import *
from graphs.pcp_graph import *


mapbox_access_token = "pk.eyJ1IjoiZ2hhaXRoOTMiLCJhIjoiY2xkM2RkZXE5MGg5bTNvbDBpdnF3YmtpYyJ9.4AMiIng35KKFYqZ9jD3a9Q"

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])


app.layout = html.Div([
	# Header
	html.Header([
		html.Div([
			html.Div([
				html.H6("Filter by:"),
				dcc.Dropdown( # Dropdown for selecting neighborhood
					id='neighborhood-dropdown',
					options=borough,
					value='New York'
				),
				
				# Numeric data: total listings, remaining listings, and average price.
				html.Div([
					html.H4(id="total_listing"),
					html.P(id = "out_of_total")
				], style={ 'display': 'inline-block', 'padding': '15px 0px 0px 10px'}),

				html.Div([
					html.H6(id="average_price")
				], style={'display': 'inline-block','padding': '0px 0px 0px 10px'}),

			], style = {'width': '27%', 'float': 'left', 'display': 'inline-block',  'padding': '5px 12px 3px 5px'}),

			html.Div([
				html.Div([
					dcc.RadioItems( # Radio buttons for room type
						id='room-type-radio',
						options=room_type,
						value=room_type[0],
						inline = True
					),
				], style = {'padding': '4px 0px 11px 9px', 'font-size': '10'}),
				
				html.Div([
					html.P("Price filter:"),
					dcc.Slider(
						min=df['price'].min(),
						max=df['price'].max(),
						step = 100,
						value=df['price'].min(),
						id='price-slider',
						marks={i: f'${i}' for i in range(df['price'].min(), df['price'].max()+50, 150)}
        		)
        		], style = {  'padding': '0px 10px 0px 8px'}),

			], style = { 'width': '60%', 'float': 'left' ,'display': 'inline-block', 'padding': '25px 0px 0px 38px'}),
		
		], style={ 'width': '65%', 'float': ' left', 'padding': '10px'}),

		html.Div([
			dcc.Graph(id="cancelation_policy_pie_chart")
		], style = {'width': '30%',  'float': 'left'}),
		
	]),
		
	
    html.Div([        
        html.Div([            
            dcc.Graph(id='map')        
            ], style={'width': '69%', 'float': 'left', 'display': 'inline'}
		),

        html.Div([
			dcc.Graph(id='room-type-bar'),
            dcc.Graph(id='night_average_figure')
            ], style={'width': '30%', 'float': 'right'}
		)
		], style={'display': 'inline-block', 'flex-direction': 'column'}
	),

	html.Div([
		dcc.Graph(id="borough_neighbourhood_counts")
	],  style={'display': 'inline', 'flex-direction': 'column'}),

	html.Div([
		dcc.Graph(id="pcp_review_rate")
	],  style={'display': 'inline', 'flex-direction': 'column'})
])

# Callback function to update the visualizations when the filters are changed
@app.callback(
    [
		Output('map', 'figure'),
     	Output('night_average_figure', 'figure'),
     	Output('room-type-bar', 'figure'),
		Output('total_listing', component_property='children'),
		Output('out_of_total',  component_property='children'),
		Output('average_price',  component_property='children'),
		Output("cancelation_policy_pie_chart", "figure"),
		Output("borough_neighbourhood_counts", 'figure'),
		Output("pcp_review_rate", "figure")
	],
    [
		Input('neighborhood-dropdown', 'value'),
     	Input('price-slider', 'value'),
     	Input('room-type-radio', 'value')
	]
)

def update_graph(neighborhood, price_range, room_type):
	# Assign the original data frame to the filtered data frame
	filtered_df = df
	# Get the latitude, longitude, and zoom level for the selected neighborhood from the borough_coordinates dictionary from data file
	lat, lon, zoom = borough_coordinates[neighborhood]

	# If the selected neighborhood is not 'New York', filter the data frame to only include listings from that neighborhood
	if neighborhood != 'New York':
		filtered_df = filtered_df[filtered_df['borough'] == neighborhood]
		lat, lon, zoom= borough_coordinates[neighborhood] 	# Update the latitude, longitude, and zoom level to match the selected neighborhood
	# If the selected price range is not the minimum price in the original data frame, filter the data frame to only include listings within that price range
	if price_range != df['price'].min():
		filtered_df = filtered_df[filtered_df.price.between(price_range, df['price'].max())]
	# If the selected room type is not 'Any', filter the data frame to only include listings with that room type
	if room_type != 'Any': 
		filtered_df = filtered_df[filtered_df['room_type'] == room_type]

	#Numerical data
	total_listing = "Total: {:,}".format(filtered_df.shape[0])
	out_of_total = "out of {:,} ({:.2f}%)".format(df.shape[0], (filtered_df.shape[0]/df.shape[0])*100)
	average_price = "Average price: ${:.2f}".format(filtered_df.price.mean())

	# Create borough neighbourhood counts graph
	borough_neighbourhood_graph = borough_neighbourhood_count(filtered_df)

	# Create a map of the listings
	map_figure = map_listings(filtered_df, lat, lon, mapbox_access_token, zoom)
	
	# Create a bar chart of the room types
	room_type_bar_figure = room_type_bar(filtered_df)

	# Create a histogram of the Average Minimum Nights per Room Type by Borough
	night_average_figure = minimum_nights_graph(filtered_df)

	# Cancelation policy pie chart
	cancellation_pie = cancellation_policy_graph(filtered_df)

	# Parallel Coordinates graph showing the relation between "number_of_reviews", "review_rate_number", and "minimum_nights"
	pcp_review_rate_plot = pcp_review_relation(filtered_df)

	return map_figure, night_average_figure, room_type_bar_figure, total_listing, out_of_total, average_price, cancellation_pie, borough_neighbourhood_graph, pcp_review_rate_plot

if __name__ == "__main__":
    app.run_server(debug=True)