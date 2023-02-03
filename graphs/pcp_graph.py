import plotly.graph_objs as go
import plotly.express as px


#Generates a parallel coordinate plot of the given dataframe.

def pcp_review_relation(filtered_df):
    pcp_review_rate_ = px.parallel_coordinates(
		filtered_df,
		color = "review_rate_number",
		dimensions = ["number_of_reviews", "review_rate_number", "minimum_nights"],
		color_continuous_scale=px.colors.sequential.Plasma,
		title="Parallel Coordinate Plot of Number of Reviews, Review Rate Number, and Minimum Nights"
	)
    pcp_review_rate_plot = go.Figure(data = pcp_review_rate_)
    return pcp_review_rate_plot