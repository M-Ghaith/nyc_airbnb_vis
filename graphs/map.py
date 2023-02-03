import plotly.graph_objs as go

def map_listings(filtered_df, lat, lon, mapbox_access_token, zoom):
    # create scattermapbox trace for marker visualization
    data = [go.Scattermapbox(
	    lat=filtered_df["lat"], 
	    lon=filtered_df["long"], 
	    mode="markers", # specify markers display mode
	    marker=go.scattermapbox.Marker(
	        size = 4, 
			sizemode = 'diameter', 
			sizeref = 0.1, 
	       	color = filtered_df["review_rate_number"], # marker color based on review_rate_number
	        colorscale = 'Viridis',
	        colorbar = dict(thickness = 10, title = "Review rate"), #
	        opacity = 0.7 
	    ),
	    text = filtered_df.name # text displayed on hover, taken from the name column of filtered_df

	)]

    # create layout for the map
    layout = go.Layout(
		width=1000, 
    	height=650, 
    	autosize=True, # automatically size the map
	    hovermode="closest", # hover display mode
		margin = dict(l = 10, r = 10, t = 10, b = 10), # margin configuration for map position on the screen
	    mapbox=go.layout.Mapbox(
	        accesstoken=mapbox_access_token, # access token obtained from Mapbox.com
	        bearing=0, # map orientation
	        center=go.layout.mapbox.Center(
	            lat=lat, # latitude of center point
	            lon=lon  # longitude of center point
	        ),
	        pitch=5, # map angle of view
	        zoom=zoom, # map zoom level
			
	    ),
	)
    # create Figure object for the map and return it
    map = go.Figure(data=data, layout=layout)
    return map