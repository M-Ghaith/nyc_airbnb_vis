import plotly.graph_objs as go


def borough_neighbourhood_count(filtered_df):
    # Group the dataframe by borough and neighbourhood columns
    borough_neighbourhood_counts = filtered_df.groupby(['borough', 'neighbourhood']).size().reset_index()
    
    # Rename the columns in the resulting dataframe
    borough_neighbourhood_counts.columns = ['Borough', 'Neighbourhood', 'Count']
    
    # Create a bar plot using Plotly
    borough_neighbourhood_data = [go.Bar(
		x = borough_neighbourhood_counts['Neighbourhood'], # x-axis data
		y = borough_neighbourhood_counts['Count'], # y-axis data
		marker = go.bar.Marker(
			color = borough_neighbourhood_counts['Borough'].astype('category').cat.codes, # color data
            colorscale = 'Viridis', # color scale
		),
		text = borough_neighbourhood_counts['Borough'], # text data
		textposition = 'auto', # position of text
		hovertext = 'Borough: ' + borough_neighbourhood_counts['Borough'] + '<br>' + 'Neighbourhood: ' + borough_neighbourhood_counts['Neighbourhood'] + '<br>' +'Count: ' + borough_neighbourhood_counts['Count'].astype(str), # hover text
	)]
    
    # Define the layout for the bar plot
    borough_neighbourhood_layout = go.Layout(
			height = 500, 
			title = "Listings Counts",
			margin = dict(l =50, r = 50, t = 50, b = 50),
		)
    
    # Create the final figure using the data and layout
    borough_neighbourhood_graph = go.Figure(data = borough_neighbourhood_data, layout = borough_neighbourhood_layout)
    
    # Return the final figure
    return borough_neighbourhood_graph