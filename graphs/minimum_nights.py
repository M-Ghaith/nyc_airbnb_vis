import plotly.graph_objs as go
import plotly.express as px

def minimum_nights_graph(filtered_df):
    # Group filtered dataframe by room type and borough, then compute the average of minimum nights
    df_average_MN_ = filtered_df.groupby(["room_type", "borough"]).agg({"minimum_nights":"mean"}).reset_index()
    # Create a bar graph to show average minimum nights per room type and borough
    night_average_trace = px.bar(
		df_average_MN_,
		x = "room_type", 
		y = "minimum_nights", 
		color = "borough", 
		title='Average Minimum Nights', 
		height = 350, 
	)
    night_average_figure = go.Figure(data=night_average_trace)
    return night_average_figure