import plotly.graph_objs as go


def cancellation_policy_graph(filtered_df):
    # Define colors for the pie chart
    colors = ['gold', 'mediumturquoise', 'lightgreen']

    # Define the layout for the pie chart
    cancellation_pie_layout = go.Layout(
        height = 200, 
        margin = dict(l =50, r = 50, t = 50, b = 50), 
        title="Cancellation Policy" 
    )
    
    # Count the number of instances of each cancellation policy
    cancellation_count = filtered_df["cancellation_policy"].value_counts()
    # Calculate the percentage of the data that each policy represents
    cancellations = ((cancellation_count/filtered_df.shape[0]) * 100).round(1)

    # Create the pie chart
    cancellation_pie = go.Figure(
        data=[go.Pie(
            # Set the labels for the pie chart to be the unique cancellation policies
            labels = filtered_df.cancellation_policy.unique(),
            # Set the values for the pie chart to be the calculated percentages
            values = cancellations
        )],
        layout = cancellation_pie_layout
    )
    # Update the chart with hover and text information and colors
    cancellation_pie.update_traces(
        hoverinfo='label+percent', # Display label and percentage when hovering over chart
        textinfo='value', # Display the value (percentage) in the chart
        textfont_size=15, # Set the font size of the value display
        marker=dict(colors=colors, line=dict(color='#000000', width=2)) # Set the color and line color and width of the pie chart
    )
    return cancellation_pie