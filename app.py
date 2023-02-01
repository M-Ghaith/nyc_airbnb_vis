import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px


from data import *


mapbox_access_token = "pk.eyJ1IjoiZ2hhaXRoOTMiLCJhIjoiY2xkM2RkZXE5MGg5bTNvbDBpdnF3YmtpYyJ9.4AMiIng35KKFYqZ9jD3a9Q"

app = dash.Dash(external_stylesheets=[dbc.themes.LUX])

app.layout = html.Div([
	#Header
	html.Header([
		html.Div([
			html.Div([
				html.H6("Filter by:"),
				dcc.Dropdown(
					id='neighborhood-dropdown',
					options=borough,
					value='New York'
				),
				#Numeric data
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
					dcc.RadioItems(
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
						marks={i: f'${i}' for i in range(df['price'].min(), df['price'].max(), 150)}
        		)
        		], style = {  'padding': '0px 10px 0px 8px'}),

			], style = { 'width': '60%', 'float': 'left' ,'display': 'inline-block', 'padding': '25px 0px 0px 38px'}),
		
		], style={ 'width': '65%', 'float': ' left', 'padding': '10px'}),

		html.Div([
			dcc.Graph(id="cancelation_policy_pie_chart")
		], style = {'width': '30%',  'float': 'left'}),
		
	]),
		
	
	#Body
    html.Div([        
        html.Div([            
            dcc.Graph(id='map')        
            ], style={'width': '69%', 'float': 'left', 'display': 'inline'}
		),

        html.Div([
			dcc.Graph(id='room-type-bar'),
            dcc.Graph(id='price-histogram')
            ], style={'width': '30%', 'float': 'right'}
		)
		], style={'display': 'inline-block', 'flex-direction': 'column'}
	),

	html.Div([
		dcc.Graph(id="borough_neighbourhood_counts")
	],  style={'display': 'inline', 'flex-direction': 'column'})
])

# Callback function to update the visualizations when the filters are changed
@app.callback(
    [
		Output('map', 'figure'),
     	Output('price-histogram', 'figure'),
     	Output('room-type-bar', 'figure'),
		Output('total_listing', component_property='children'),
		Output('out_of_total',  component_property='children'),
		Output('average_price',  component_property='children'),
		Output("cancelation_policy_pie_chart", "figure"),
		Output("borough_neighbourhood_counts", 'figure')
	],
    [
		Input('neighborhood-dropdown', 'value'),
     	Input('price-slider', 'value'),
     	Input('room-type-radio', 'value')
	]
)

def update_graph(neighborhood, price_range, room_type):
	filtered_df = df
	lat, lon, zoom = borough_coordinates[neighborhood]
	if neighborhood != 'New York':
		filtered_df = filtered_df[filtered_df['borough'] == neighborhood]
		lat, lon, zoom= borough_coordinates[neighborhood]
	if price_range != df['price'].min():
		filtered_df = filtered_df[filtered_df.price.between(price_range, df['price'].max())]
	if room_type != 'Any':
		filtered_df = filtered_df[filtered_df['room_type'] == room_type]

	#Numerical data
	total_listing = "Total: {:,}".format(filtered_df.shape[0])
	out_of_total = "out of {:,} ({:.2f}%)".format(df.shape[0], (filtered_df.shape[0]/df.shape[0])*100)
	average_price = "Average price: {:.2f}".format(filtered_df.price.mean())

	# Create borough neighbourhood counts graph
	borough_neighbourhood_counts = filtered_df.groupby(['borough', 'neighbourhood']).size().reset_index()
	borough_neighbourhood_counts.columns = ['Borough', 'Neighbourhood', 'Count']

	borough_neighbourhood_data = [go.Bar(
		x = borough_neighbourhood_counts['Neighbourhood'],
		y = borough_neighbourhood_counts['Count'],
		marker = go.bar.Marker(
			color = borough_neighbourhood_counts['Borough'].astype('category').cat.codes,
            colorscale = 'Viridis',
		),
		text = borough_neighbourhood_counts['Borough'],
		textposition = 'auto',
		hovertext = 'Borough: ' + borough_neighbourhood_counts['Borough'] + '<br>' + 'Neighbourhood: ' + borough_neighbourhood_counts['Neighbourhood'] + '<br>' +'Count: ' + borough_neighbourhood_counts['Count'].astype(str),
	)]
	borough_neighbourhood_layout = go.Layout(
			height = 500, 
			title = "Listings Counts",
			margin = dict(l =50, r = 50, t = 50, b = 50),
			
		)
	borough_neighbourhood_graph = go.Figure(data = borough_neighbourhood_data, layout = borough_neighbourhood_layout)
	# Create a map of the listings
	data = [go.Scattermapbox(
	    lat=filtered_df["lat"],
	    lon=filtered_df["long"],
	    mode="markers",
	    marker=go.scattermapbox.Marker(
	        size = 3,
	       	color = filtered_df["review_rate_number"],
	        colorscale = 'Viridis',
	        colorbar = dict(thickness = 10, title = "Review rate"),
	        opacity = 0.7
	    ),
	    text = filtered_df.name

	)]
	layout = go.Layout(
		width=1000,
    	height=650,
    	autosize=False,
	    hovermode="closest",
		margin = dict(l = 10, r = 10, t = 10, b = 10),
	    mapbox=go.layout.Mapbox(
	        accesstoken=mapbox_access_token,
	        bearing=0,
	        center=go.layout.mapbox.Center(
	            lat=lat,
	            lon=lon
	        ),
	        pitch=5,
	        zoom=zoom,
			
	    ),
	)

	figure = go.Figure(data=data, layout=layout)

	# Create a histogram of the prices
	price_histogram_trace = go.Histogram(x=filtered_df['price'], nbinsx=20)
	price_histogram_layout = go.Layout(
		title='Price Histogram', 
		margin = dict(l =50, r = 50, t = 50, b = 50),
		height = 350, 
		)
	price_histogram_figure = go.Figure(data=[price_histogram_trace], layout=price_histogram_layout)

	# Create a bar chart of the room types
	room_type_counts = df.groupby(["room_type", "instant_bookable"]).size().reset_index()
	room_type_counts.columns = ["room_type", "instant_bookable", "count"]

	room_type_bar_trace = px.bar(
			x=room_type_counts["room_type"], 
			y=room_type_counts["count"],
			color = room_type_counts["instant_bookable"],
		)
	room_type_bar_layout = go.Layout(
		title='Room Type Counts',	
		margin = dict(l =50, r = 50, t = 50, b = 50),
		height = 300,
		)
	room_type_bar_figure = go.Figure(data=room_type_bar_trace, layout=room_type_bar_layout)

	# cancelation_policy_pie_chart
	colors = ['gold', 'mediumturquoise', 'lightgreen']
	cancellation_pie_layout = go.Layout(
		height = 200, 
		margin = dict(l =50, r = 50, t = 50, b = 50),
		title="Cancellation Policy"
		)

	cancellation_count = filtered_df["cancellation_policy"].value_counts()
	cancellations = ((cancellation_count/filtered_df.shape[0]) * 100).round(1)

	cancellation_pie = go.Figure(
		data=[go.Pie(
			labels = filtered_df.cancellation_policy.unique(),
			values = cancellations
		)],
		layout = cancellation_pie_layout
	)
	cancellation_pie.update_traces(
		hoverinfo='label+percent', 
		textinfo='value', 
		textfont_size=20,
        marker=dict(colors=colors, line=dict(color='#000000', width=2))
		)

	return figure, price_histogram_figure, room_type_bar_figure, total_listing, out_of_total, average_price, cancellation_pie, borough_neighbourhood_graph

if __name__ == "__main__":
    app.run_server(debug=True)




