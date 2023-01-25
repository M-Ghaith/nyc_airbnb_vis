# NYC Airbnb Listings Dashboard
This is a Dash application that allows users to view the location of Airbnb listings in New York City on a map and filter the listings by borough. The dashboard also includes a bar graph that displays the distribution of room types.

## Features
Interactive map that displays the location of each Airbnb listing in New York City
Hovering over a data point on the map displays the listing's price and average review
Dropdown menu that allows users to filter the map by borough
Bar graph that displays the distribution of room types

# Getting Started

## Prerequisites

Plotly and Dash for building the interactive dashboard
Pandas for loading and handling the dataset
A Mapbox access token

##Installing

Clone the repository
`git clone https://github.com/M-Ghaith/nyc-airbnb-vis.git`

## Install the required libraries

`pip install -r requirements.txt`

Replace YOUR_MAPBOX_TOKEN in the code with your actual Mapbox token.

Make sure the csv file 'nyc_airbnb.csv' exist in the same location as the code.

## Running the application

Run the application
`python app.py`
Open a browser and navigate to http://localhost:8050/ to view the dashboard

## Built With
Dash - The web framework used
Plotly - (https://plotly.com/) - Used for creating the interactive map and bar graph

Pandas - Used for loading and handling the dataset
Mapbox - Used for providing the map tiles and locations data

## Authors
Ghaith 

## Note
The dataset used in this project is just a sample data and doesn't reflect the actual data from the Airbnb website, thus the prices and reviews may not be accurate.
This project is only for educational and learning purposes.

## License
This project is licensed under the MIT License - see the LICENSE.md file for details.
