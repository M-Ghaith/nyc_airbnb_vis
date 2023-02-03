import plotly.graph_objs as go
import plotly.express as px

def room_type_bar(filtered_df):
    room_type_counts = filtered_df.groupby(["room_type", "borough"]).size().reset_index(name='counts')
    room_type_bar_trace = px.bar(
			room_type_counts,
			y="counts",
			x="room_type",
			color = "borough",
			height = 350,
			title = "Room Type per Borough Count"

		)
    room_type_bar_figure = go.Figure(data=room_type_bar_trace)
    return room_type_bar_figure