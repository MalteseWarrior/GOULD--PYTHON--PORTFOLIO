## Welcome to FlyBuy!
# This is a streamlit python application that allows you to search for flights at real time using OpenSky API.
# Along with the flight data, it also provides details about the flight vehicle, such as its model, manufacturer, and other details.
# With this, the user is given the opportunity to analyze the average fare cost of the flight, and the average costs of actually flying the aircraft.

# As a note for clarity, the majoirty of html and css code was made with the help of ChatGPT.
# The fonts and layout was much quicker to create this way, I know the commands but it would have taken a lot longer to create the same layout and design.

## ------ WAIT! ------ ##
# Before running the code, make sure you have the required libraries installed. Especially if you are using a virtual environment.
# This is warning is for all you local users out there. If you are using the streamlit community cloud, you can ignore this warning.


## ------ LET'S GET STARTED! ------ ##
## Importing Libraries
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# These ones are for the OpenSky API
import requests
import calendar
import logging
import pprint
import time
from collections import defaultdict
from datetime import datetime
import random

# Access OpenSky API and Data Files
URL = 'https://opensky-network.org/api/'
JetFuelData = pd.read_csv('JetFuelData.csv')
CountryCoords = pd.read_csv('country-coord.csv')


# Clean JetFuelData
# Remove empty columns (0, NaN, --, etc.)

JetFuelData = JetFuelData.dropna(axis=1, how='all')


# Create Map For Data Associated with Flight
# This will be done by creating a tab for each analysis type
# Front page will be live map of flights in the air with discussion of the data
# Second tab focuses on Jet Fuel Per Country

# Create First Tab - Having Tuple Issue with st.tabs()

st.title("FlyBuy - Flight Data Analysis")

# Formatting Later


st.info("Let the Time Fly By as you Wait!")
# Fetch from OpenSky API


try:
    response = requests.get(URL + "states/all", timeout=10)
    data = response.json()
    timestamp = datetime.utcfromtimestamp(data['time']).strftime('%Y-%m-%d %H:%M:%S UTC') # Not sure why deprecated
    st.success(f"Data fetched successfully at {timestamp}")

    # Flight Specifics
    Live_Data_Call = [
        "icao24", "callsign", "origin_country", "time_position", "last_contact", "longitude",
        "latitude", "baro_altitude", "on_ground", "velocity", "heading", "vertical_rate",
        "sensors", "geo_altitude", "squawk", "spi", "position_source"
    ]


    df = pd.DataFrame(data['states'], columns=Live_Data_Call)

    # Clean Live Data
    df = df[df["on_ground"] == False] # Only show flights in the air
    df["callsign"] = df["callsign"].str.strip() # Apparently some callsigns have whitespace at the end, so we need to remove it
    df = df.dropna(subset=["longitude", "latitude", "callsign"]) # Remove rows with NaN values in longitude and latitude columns


    # Provide Filter so User can parse through the live data
    # Use st.selectbox to create a filter for the data
    # Allows by country and by flight
    country_filter = st.selectbox("Select a Country", options=["All"] + df["origin_country"].unique().tolist())
    # flight_filter = st.selectbox("Select a Flight", options=["All"] + df["callsign"].unique().tolist()) - Was Not Accurate

    if country_filter != "All":
        df = df[df["origin_country"] == country_filter]
    # if flight_filter != "All":
       # df = df[df["callsign"] == flight_filter]


    # Create fun way to display amount of flights in the air
    st.metric(label="Total Flights in the Air", value=len(df))

    
   


    # Add a map to show the flights in the air, originally with st.map()
    # pydeck was much coolor looking and more advanced than st.map()
    # Assign Colors to Origin Country
    # Develop color directory for countries defined by the origin_country coulumn from OpenSky API
    # Random each time

    # Generate random colors for each origin country
    # Generate RGB colors for each origin country
    unique_countries = df["origin_country"].unique()
    country_colors = {
        country: np.random.randint(0, 256, size=3).tolist() for country in unique_countries
    }
    df["color"] = df["origin_country"].map(country_colors)

    tooltip = {
        "html": "<b>Callsign:</b> {callsign}<br><b>Origin Country:</b> {origin_country}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }

    # Use pydeck for a more advanced map visualization with colors
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["longitude", "latitude"],
        get_fill_color="color",
        get_radius=10000,
        pickable=True,
        auto_highlight=True,  # Enable hover highlighting
    )

    view_state = pdk.ViewState(
        latitude=df["latitude"].mean(),
        longitude=df["longitude"].mean(),
        zoom=3,
        pitch=0,
    )

    # Add the tooltip to the pydeck chart
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    )

    st.pydeck_chart(deck)

except Exception as e:
    st.error(f"Error fetching data: {e}")
    logging.error(f"Error fetching data: {e}")


        

    