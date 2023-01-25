import dash
from dash import html, dcc
import plotly.graph_objs as go
from dash.dependencies import Input, Output

from data import *

mapbox_access_token = "pk.eyJ1IjoiZ2hhaXRoOTMiLCJhIjoiY2xkM2RkZXE5MGg5bTNvbDBpdnF3YmtpYyJ9.4AMiIng35KKFYqZ9jD3a9Q"

app = dash.Dash()

app.layout = html.Div([
    html.H1('New York Airbnb Listings'),
    html.Div([
    	html.Div([
    		dcc.Dropdown(
	            id='neighborhood-dropdown',
	            options=borough,
	            value='New York'
        	)
		], style = {'padding': '0px 30px 20px 20px'}),
        
        html.Div([
        	 dcc.Slider(
	            min=df['price'].min(),
	            max=df['price'].max(),
	            step = 50,
	            value=df['price'].min(),
	            id='price-slider',
	            marks={i: f'${i}' for i in range(df['price'].min(), df['price'].max()+50, 50)}
        	)
        ], style = {'padding': '0px 0px 20px 20px'})
        
    ], style = {'width': '80%', 'display': 'inline-block'}),

     html.Div([
        	dcc.RadioItems(
	            id='room-type-radio',
	            options=room_type,
	            value=room_type[0]
        	)
    	], style = {'display': 'inline-block', 'padding': '0px 30px 20px 20px'}),

    html.Div([
    		dcc.Graph(id='map')
    	]),

    html.Div([
    	    dcc.Graph(id='price-histogram')
    	],  style = {'width': '49%' , 'display': 'inline-block'}),
    html.Div([
    	    dcc.Graph(id='room-type-bar')
    	],  style = {'width': '49%' , 'display': 'inline-block'})
])



# Callback function to update the visualizations when the filters are changed
@app.callback(
    [
		Output('map', 'figure'),
     	Output('price-histogram', 'figure'),
     	Output('room-type-bar', 'figure')
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

	# Create a map of the listings
	data = [go.Scattermapbox(
	    lat=filtered_df["lat"],
	    lon=filtered_df["long"],
	    mode="markers",
	    marker=go.scattermapbox.Marker(
	        size = 4,
	       	color = filtered_df["review_rate_number"],
	        colorscale = 'Earth',
	        colorbar = dict(thickness = 10, title = "Review rate"),
	        opacity = 0.7
	    ),
	    text = filtered_df.name

	)]

	layout = go.Layout(
		width=1400,
    	height=700,
    	autosize=False,
	    hovermode="closest",
	    mapbox=go.layout.Mapbox(
	        accesstoken=mapbox_access_token,
	        bearing=0,
	        center=go.layout.mapbox.Center(
	            lat=lat,
	            lon=lon
	        ),
	        pitch=5,
	        zoom=zoom,
			transition = {'duration': 1000, 'easing': 'cubic-in-out'}
	    ),
	)

	figure = go.Figure(data=data, layout=layout)

	figure.update_traces(
		cluster_maxzoom=12, 
		cluster_color="darkblue", 
		cluster_opacity=0.5, 
		cluster=dict(enabled=False),
		cluster_size= 15
		)

	# Create a histogram of the prices
	price_histogram_trace = go.Histogram(x=filtered_df['price'], nbinsx=20)
	price_histogram_layout = go.Layout(title='Price Histogram')
	price_histogram_figure = go.Figure(data=[price_histogram_trace], layout=price_histogram_layout)

	# Create a bar chart of the room types
	room_type_counts = filtered_df['room_type'].value_counts()
	room_type_bar_trace = go.Bar(x=room_type_counts.index, y=room_type_counts.values)
	room_type_bar_layout = go.Layout(title='Room Type Counts')
	room_type_bar_figure = go.Figure(data=[room_type_bar_trace], layout=room_type_bar_layout)

	return figure, price_histogram_figure, room_type_bar_figure

if __name__ == "__main__":
    app.run_server(debug=True)




