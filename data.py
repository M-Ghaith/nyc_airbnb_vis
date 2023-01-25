import os
import pandas as pd
import numpy as np

df = pd.read_csv(os.getcwd()+ '/database/airbnb_data.csv', low_memory=False)

df.price = df.price.astype("Int64")

borough = df["borough"].unique()
borough = list(borough)
borough.insert(0, "New York")

borough_coordinates = {"Manhattan": (40.78, -73.966, 10.5),
                       "Brooklyn": (40.6453531, -74.0150374, 10.5),
                       "Queens": (40.7282, -73.7949, 10.5),
                       "Bronx": (40.836, -73.872, 11),
                       "Staten Island": (40.589, -74.087,10.8),
                       "New York": (40.738, -73.98, 9.3)
                       }

room_type = df['room_type'].unique()
room_type = list(room_type)
room_type.insert(0, "Any")