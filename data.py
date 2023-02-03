import os
import pandas as pd

current_directory = os.getcwd()

# Read the Airbnb data from the csv file into a pandas dataframe

try:
    df = pd.read_csv(current_directory + '/database/airbnb_data.csv', low_memory=False)
except FileNotFoundError:
    print("Error: The file could not be found. Please check the path and try again.")


# Convert the price column in the dataframe to Int64 type
df.price = df.price.astype("Int64")

# Create a list of unique boroughs present in the data
borough = df["borough"].unique()
borough = list(borough)
borough.insert(0, "New York") # Add "New York" to the beginning of the borough list

# Create a dictionary of borough coordinates with the keys being the borough names
borough_coordinates = {"Manhattan": (40.78, -73.966, 10.5),
                       "Brooklyn": (40.6453531, -74.0150374, 10.5),
                       "Queens": (40.7282, -73.7949, 10.5),
                       "Bronx": (40.836, -73.872, 11),
                       "Staten Island": (40.589, -74.087,10.8),
                       "New York": (40.738, -73.98, 9.3)
                       }

# Create a list of unique room types 
room_type = df['room_type'].unique()
room_type = list(room_type)
room_type.insert(0, "Any") # Add "Any" to the beginning of the room type list
