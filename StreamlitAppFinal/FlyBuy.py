## Welcome to FlyBuy!

## ------- PlEASE READ THE README ------- ##
# Before proceeding please go back to the repository and read the read me...
# If you did not, this is a brief summary:

# This is a streamlit python application that allows you to search for flights at real time using OpenSky API.
# Along with the flight data, it also provides details about the airports in the United States as it is the origin country with the most
# departure flights BY FAR. With this, the location and total flight departures relative to airport codes are displayed in both a bar chart and a proportional map.
# With this, flight delay data was combined with average fare per airport to construct a quick and interactive analysis on how much revenue an airport generates with respect
# to 2024 Bureau of Transportation data. 
# With this, the user is given the opportunity to analyze the average fare cost of the flight, and the amount delays actually cost an aiport relative to the fare price.
# In other words, this app was created with the intention of recognizing flight departure patterns and how much different delays impact the final revenue of an airport in the
# country with the largest departure flights in the world, The United States.


## ------- User Inputs, Main Functions, and Outputs ------- ##
# Page 1:
    # Presents a pydeck map that displays live flight data by call sign and country of origin
    # Presents a live number of the amount of active departures in the world
    # The User may specify the country of origin for analysis
    # Plotly barchart is provided for active comparison between countries

# Page 2:
    # Presents a proportional plot map using pydeck to visualize 2024 airport data in the United States
    # Emphasizes airports relative to their total flight departures annually
    # User may use a slidebar to go between the minimum to maximum flight departures in the data to see which airports fit in that range
    # Sidebar provides extra information that alludes to the third page as it gives information on the selected airport's delays and average fare

# Page 3:
    # A user-friendly calculator that allows the user to see how much delays will cost a respective airport per delayed passenger
    # The numbers were calculated with industry standards (its costs approximately $13 per delayed passenger)
    # The amount of money lost is approximated using the delay likelihood at the selected aiport
    # For a visualization of the relationship between total passengers, delayed passengers, gross revenue, and net revenue a Sankey diagram was constructed
    # Sankey digram is an attempt to visualize the contribution of delays to the net revenue - interestingly they contribute little despite high fares

## ------- CLARIFICATION ------ ##
# As a note for clarity, the majoirty of html and css code was made with the help of ChatGPT.
# The fonts and layout was much quicker to create this way, I know the commands but it would have taken a lot longer to create the same layout and design.
# This also goes for the formatiting of visual representations, I originally used the innate capabilities of streamlit but with formatting help from AI
# I expanded beyond that and implemented some seperate visual libraries - provided an opportunity to learn plotly and pydeck
# I used ChatGPT because I wanted the opportunity to have the time to learn beyond my already existing toolkit, its a tool to explore what I would not otherwise be exposed to /
# Library wise in this 


##  ------- SPECIAL THANKS  ------- ##
# Special thanks to these websites and organizations for their help in constructing this app
    #  Geeksforgeeks: https://www.geeksforgeeks.org/
    #  Pydeck: https://deckgl.readthedocs.io/en/latest/deck.html
    #  Pydeck (again): https://deckgl.readthedocs.io/en/latest/gallery/scatterplot_layer.html
    #  Plotly: https://plotly.com/python/sankey-diagram/
    #  Plotly (again): https://plotly.com/python/bar-charts/
    #  ChatGPT: The app would not look this good without it (Which means I need to learn css at some point)

# And of course thank you to Professor Smiley who helped me learn so much more about python and data analysis
# I greatly appreciate the opportunities he provided me to expand my knowledge in this space, even when my ideas were too above and beyond at times



## ------ WAIT! ------ ##
# Before running the code, make sure you have the required libraries installed. Especially if you are using a virtual environment.
# This is warning is for all you local users out there. If you are using the streamlit community cloud, you can ignore this warning.

# This app is up on the streamlit community, visit the repository that took you to this code for that link
# Otherwise, if you wish to launch this locally you will need to connect to an environment that includes all of the libraries down below
# If in an anaconda environment (what I use) you can activate your environment in the anaconda prompt and then write:

# pip install streamlit
# pip install pandas
# pip install numpy
# pip install pydeck
# pip install plotly
# pip install streamlit-plotly-events
# pip install requests

# Once this is done, connect to your environment and use the cd command (if you are using a program like VS code) to open the file location
# Once you are in the file location with FlyBuy.py and the associated data files, use the command:
# streamlit run FlyBuy.py



## ------ LET'S GET STARTED! ------ ##
## Importing Libraries
import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import plotly.graph_objects as go
import streamlit_plotly_events


# These ones are for the OpenSky API
import requests
import calendar
import logging
import pprint
import time
from collections import defaultdict
from datetime import datetime
import random

## ---------- Markdown Formatting for Pages ------------ ##
st.set_page_config(page_title="FlyBuy", layout="wide", page_icon="✈️") # SO MUCH BETTER THAN THE NORMAL FORMAT omg

st.markdown("""
<style>
/* Base font and layout */
html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
    background-color: #f7faff;
    color: #1a1a1a;
}

/* Central container */
.block-container {
    padding: 2rem 3rem;
    max-width: 1400px;
    margin: auto;
    background-color: #ffffff;
    border-radius: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}

/* Headings */
h1, h2, h3 {
    color: #003f5c;
    font-weight: 700;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #e6f2ff;
    border-right: 2px solid #99ccff;
    padding: 1.5rem 1rem;
}

/* Metric Cards */
div[data-testid="stMetric"] {
    background-color: #f0f8ff;
    padding: 16px;
    border-radius: 10px;
    margin-bottom: 12px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

/* Input widgets */
div[class*="stSelectbox"], div[class*="stNumberInput"], div[class*="stSlider"] {
    background-color: #f4faff;
    border-radius: 10px;
    padding: 12px;
    margin-top: 6px;
    margin-bottom: 12px;
}

/* Expanders */
.streamlit-expanderHeader {
    font-size: 18px;
    color: #005c99;
    font-weight: bold;
}

/* Tooltip styling (deck.gl) */
.deck-tooltip {
    background-color: #005c99;
    color: white;
    padding: 8px;
    border-radius: 6px;
}

/* Map container border */
.custom-map-container {
    border: 3px solid #99ccff;
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 1rem;
    margin-bottom: 2rem;
}

/* --------- SLIDER STYLING ----------- */
div[data-testid="stSlider"] > div {
    color: #003f5c; /* Number label text */
}

div[data-testid="stSlider"] input[type="range"]::-webkit-slider-thumb {
    background-color: #003f5c; /* Thumb knob */
    border: 2px solid #ffffff;
}

div[data-testid="stSlider"] input[type="range"]::-webkit-slider-runnable-track {
    background: linear-gradient(to right, #a6c8ff, #005c99); /* Track gradient */
    height: 6px;
    border-radius: 6px;
}

div[data-testid="stSlider"] {
    background-color: #f0f8ff;
    padding: 16px;
    border-radius: 10px;
}

/* Firefox slider support */
div[data-testid="stSlider"] input[type="range"]::-moz-range-thumb {
    background-color: #003f5c;
    border: 2px solid #ffffff;
}

div[data-testid="stSlider"] input[type="range"]::-moz-range-track {
    background: linear-gradient(to right, #a6c8ff, #005c99);
    height: 6px;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)




# Access OpenSky API and Data Files: https://opensky-network.org/data/api
# Provided definitions and vector information that the live data contains
# More API documentation (information on vectors): https://openskynetwork.github.io/opensky-api/

URL = 'https://opensky-network.org/api/'

CountryCoords = pd.read_csv('country-coord.csv') # Coordinates of Countries for Map

# Sourced from Oepndatasoft: https://www.opendatasoft.com/en/
AirportCoords = pd.read_csv('AirportCodeCoords.csv', sep=';') # Coordinates of Airports by Airport Code United States

# Need to clean AirportCodes since formatting has the first column as:
# Airport Code;Airport Name;City Name;Country Name;Country Code;Latitude;Longitude;World Area Code;City Name geo_name_id;Country Name geo_name_id;coordinates
# Separation by colon should work, column 1 is Airport Code, Column 6 is Latitude, Column 7 is Longitude


# Sourced from Bureau of Transportation Statistics: https://www.bts.gov/
# Will Assist with United States Delay and Cost Analysis

# Many of these data files had extra, unnecessary data that could be removed manually once downloading the file
# I provided links to the organizations the data was sourced from so users can see original data

DelayCauses = pd.read_csv('Airline_Delay_Cause.csv') # Airline Delay Causes

# Departure Columns of import are Column 3 for Airport Code (Origin Airport) and Column 4 for Total Departures - Proportional map
# Depature Columns of impport are column 8 for Total Passengers/Flight, Column 9 for Total Seats/Flight - For Fare Analysis

AirPortDeparture = pd.read_csv('Departures_Airport.csv') # Departure Airports
FareCosts = pd.read_csv('AverageFare_Annual_2024.csv') # Average Fare Costs

Fare_Delay = pd.read_csv('Fare_Delay_Merge.csv')

# Data for calculator
CalculatorData = pd.read_csv('Airport_Delay_Cost_Data.csv') # Data for Calculator



# Create Map For Data Associated with Flight
# This will be done by creating a tab for each analysis type
# Front page will be live map of flights in the air with discussion of the data
# Second tab focuses on Jet Fuel Per Country

# Create First Tab - Having Tuple Issue with st.tabs()
# changes tab to st.radio() to avoid tuple issue

page = st.radio("Select View", ["Live Flight Data", "United States Delay Analysis - 2024 Data", "Revenue & Delay Calculator - 2024 Data"], horizontal=True)




if page == "Live Flight Data":
    
    st.title("FlyBuy - Live Flight Data Analysis")


    st.info("Let the Time Fly By as you Wait!")
    # Add page and app details for user comprehension
    # Provided summary to Chatgpt, returned to me a pleasanlty formatted version
    with st.expander("📘 Page Details:"):
        st.markdown("""
        ### ✈️ **FlyBuy Application Overview**

        **FlyBuy** is a real-time air traffic and airport analysis platform that draws from global and domestic aviation data sources. The application is built to:

        - 🌍 Visualize **live departures around the world**
        - 🛬 Highlight the **United States’ dominant role in global air traffic**
        - 🏙️ Drill into **U.S. airport-level metrics**, especially delays
        - 💸 Assess the **economic costs of those delays**

        By integrating the OpenSky API with datasets from the Bureau of Transportation Statistics, FlyBuy creates a comprehensive, interactive lens on air travel activity and performance.

        ---

        ### 🌐 **Live Flight Data Page**

        This page connects to the **OpenSky Network API** to display **live global flights** that are currently in the air.

        **Key Features:**
        - 📍 **Interactive flight map** showing airborne aircraft, color-coded by their origin country
        - 🌐 **Country filter** to narrow down flights by country of origin
        - 📊 **Live flight count** with metric updates
        - 📈 **Bar chart** displaying flight volume per country

        **Why It Matters:**
        The U.S. has the **largest share of active airborne flights globally**. This foundational insight motivates deeper analysis into:
        - 🛫 U.S. airports with the most departures
        - ⏱️ Delay frequencies and causes
        - 💵 The financial impact of delays on airlines and travelers
        """)
         
    # Fetch from OpenSky API - Done with the help of OpenSky pythong repository and some error fixes provided by AI (was only getting certain countries for a while)
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


        # May not be the best idea, but I thought it was fun, if user wants to change this create concrete list... I did not want to do that for every country
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
            tooltip=tooltip,
            map_style="mapbox://styles/mapbox/light-v10",# Chatgpt helped me find this formatting
            map_provider="mapbox",
        )
        
        st.markdown('<div class="custom-map-container">', unsafe_allow_html=True)
        st.pydeck_chart(deck, use_container_width=True, height=650)
        st.markdown('</div>', unsafe_allow_html=True)

        # Originally st.bar_chart, reformatted with plotly
        bar_data = df["origin_country"].value_counts().reset_index()
        bar_data.columns = ["Country", "Flights"]

        custom_blues = [
            "#c6dbef",  # muted blue-gray
            "#9ecae1",  # mid-light blue
            "#6baed6",  # mid blue
            "#4292c6",  # rich blue
            "#2171b5",  # bold blue
            "#084594"   # dark navy
        ]

        fig_bar = px.bar(
            bar_data,
            x="Country",
            y="Flights",
            color="Country",
            color_discrete_sequence=custom_blues,
            title="Flights by Country"
        )

        fig_bar.update_layout(
            plot_bgcolor="white",
            xaxis_title=None,
            yaxis_title="Number of Flights",
            title_font_size=20
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        logging.error(f"Error fetching data: {e}")

# From the OpenSky API, it is clear the United States has the most flights in the air
# Cause for analysis into the most delays in the US

# ----------------------------------- This page will be a map of the US with proportional circles ------------------------------- #


# This section will be conduected on the second tab and will include a map of the US with proportional circles
# Circles are proportional to the amount of flights per year, create over and side bar to show relavent delays



elif page == "United States Delay Analysis - 2024 Data":
    try:
        st.title("FlyBuy - United States Aiport Analysis")
        st.info("Doesn't time just Fly By? " \
        "Locating the U.S Airports with the Most Flights in 2024")

        with st.expander("📘 Page Details:"):
                    st.markdown("""
                    This page provides an analysis of the airports in the United States with the most flights in 2024.  \
                    The analysis includes a map with proportional circles representing the number of flights,  \
                    For the sidebar, you can select an airport to view its details, including the average fare cost and delay causes.\
                    Here are some relevant definitions:     
                                        
                    **✈️ Flight Activity**
                    - **Total Departures:** Number of flights that took off from the airport in 2024.
                    - **Total Flights Tracked:** Number of arrival records tracked for the airport.
                    - **Cancellations:** Flights that were scheduled but ultimately did not operate.
                    - **Diversions:** Flights that did not land at their intended destination airport.

                    **🕒 Delay Metrics**
                    - **Delayed Flights (>15 min):** Flights that arrived 15+ minutes later than their scheduled arrival time.
                    - **Carrier Delay:** Delays caused by the airline's own operations (e.g., crew or aircraft turnaround).
                    - **Weather Delay:** Delays due to significant weather conditions preventing timely operations.
                    - **NAS Delay:** Delays attributed to the National Aviation System, including air traffic control or crowded airports.
                    - **Security Delay:** Delays caused by airport security procedures or breaches.
                    - **Late Aircraft Delay:** Delays caused by a previous flight arriving late, delaying the next departure using the same aircraft.

                    **💸 Fare Info**
                    - **Average Fare (2024):** The average ticket price for flights departing from the airport, based on BTS data.
                    """)

        # Create dataframe for the plotting on pydeck
        # Will be based on the Aiport code, airport code coordinates, and proportional circles based on the amount of flights
        # This is done with the AirportCoords dataframe, AirportDeparture dataframe, column 1 is Airport Code, Column 6 is Latitude, Column 7 is Longitude
        # from AirportCoords and want Column 3 for Airport Code (Origin Airport) and Column 4 for Total Departures from AirportDeparture
        # Proved easier and quicker to do outiside of python
        map_data = pd.read_csv('Merged_Airport_Flight_Data.csv')

        # Create pydeck map with the merged data
        map_data["radius"] = map_data["Total Departures"] / 1.5 # Adjust if needed

        # Color randomizer from ChatGPT
        # Assign unique random colors to each airport code
        unique_airports = map_data["Origin Airport Code"].unique()
        airport_colors = {
            code: np.random.randint(0, 256, size=3).tolist() for code in unique_airports
        }
        map_data["color"] = map_data["Origin Airport Code"].map(airport_colors)

        # Slider bar for user interaction
        min_departures = int(map_data["Total Departures"].min())
        max_departures = int(map_data["Total Departures"].max())
        selected_departures = st.slider(
            "Select Departure Range",
            min_value=min_departures,
            max_value=max_departures,
            value=(min_departures, max_departures),
            step=1000
        )
        # Filter data based on slider selection
        filtered_data = map_data[
            (map_data["Total Departures"] >= selected_departures[0]) &
            (map_data["Total Departures"] <= selected_departures[1])
        ]

        # Include map in filtred data
        if not filtered_data.empty:
            filtered_data["radius"] = filtered_data["Total Departures"] / 1.5 # Adjust if needed
            filtered_data["color"] = filtered_data["Origin Airport Code"].map(airport_colors)


            # Create layer
            prop_layer = pdk.Layer(
                "ScatterplotLayer",
                data=filtered_data,
                get_position=["Longitude", "Latitude"],
                get_fill_color="color",
                get_radius="radius",
                pickable=True,
                auto_highlight=True,
            )

            # Create view state
            view_state = pdk.ViewState(
                latitude=map_data["Latitude"].mean(),
                longitude=map_data["Longitude"].mean(),
                zoom=2.5,
                pitch=0,
            )
        
            # Create tooltip - similar to the one above
            tooltip = {
                "html": "<b>Airport Code:</b> {Origin Airport Code}<br><b>Total Departures:</b> {Total Departures}",
                "style": {"backgroundColor": "steelblue", "color": "white"}
            }

            # Display
            st.markdown('<div class="custom-map-container">', unsafe_allow_html=True)
            st.pydeck_chart(pdk.Deck(
                layers=[prop_layer],
                initial_view_state=view_state,
                tooltip=tooltip,
                map_style="mapbox://styles/mapbox/light-v10",
                map_provider="mapbox"),
                use_container_width=True, height=650

            )
            st.markdown('</div>', unsafe_allow_html=True)

            # Display barchart associated with the filtered data
            # Figure out how to make colors on the filtered data associated with the airport code

            st.subheader("Airports Within the Selected Departure Range")
            # Originally st.bar_chart, reformatted with plotly
            airport_bar_data = (
                filtered_data.sort_values("Total Departures", ascending=False)
            )

            custom_blues = [
                "#c6dbef",  # muted blue-gray
                "#9ecae1",  # mid-light blue
                "#6baed6",  # mid blue
                "#4292c6",  # rich blue
                "#2171b5",  # bold blue
                "#084594"   # dark navy
            ]


            # Create Plotly bar chart
            fig_airport_bar = px.bar(
                airport_bar_data,
                x="Origin Airport Code",
                y="Total Departures",
                color="Origin Airport Code",
                color_discrete_sequence=custom_blues,
                title="✈️ Departures by U.S. Airport",
            )

            # Optional layout customization
            fig_airport_bar.update_layout(
                plot_bgcolor="white",
                xaxis_title=None,
                yaxis_title="Total Departures",
                title_font_size=20,
                xaxis_tickangle=-45,
                uniformtext_minsize=8,
                uniformtext_mode='hide',
                margin=dict(t=50, b=100),
            )

            st.plotly_chart(fig_airport_bar, use_container_width=True)
            # when the user clicks on a bubble, create sidebar with information about the airport including delay causes and likelihood of delay
            # name of airport along with airport code, total departures, and average fare cost
            # Delay information and full airport name found in the Airline_Delay_Cause.csv file, but average fare cose is in AverageFare_Annual_2024.csv
            # Merge the dataframes to get the average fare cost for each airport code
            # Dataframes were strange, so I had to merge them outside of python

            # Bubbles do not have click events, so I will have a st.selectbox to select the airport code and then display
            # a sidebar with information about the airport including delay causes
            # Select an airport from the dropdown
            # Move selectbox into the sidebar otherwise page is WAYYY to cluttered
            st.sidebar.header("Aiport Details Explorer")
            selected_code = st.sidebar.selectbox("Select an Airport Code", options=filtered_data["Origin Airport Code"].unique(), key="airport_code_selectbox")


            # Standardize merge fields
            map_data["Origin Airport Code"] = map_data["Origin Airport Code"].str.strip().str.upper()
            Fare_Delay["airport"] = Fare_Delay["airport"].str.strip().str.upper()

            # Merge to enrich data
            airport_info = pd.merge(
                map_data, 
                Fare_Delay, 
                left_on="Origin Airport Code", 
                right_on="airport", 
                how="left"
            )

            # Show sidebar info - I had chaptgpt write the definitions from the xls (faster)
            if selected_code:
                st.sidebar.subheader(f"🛫 Airport Code: {selected_code}")
                selected_row = airport_info[airport_info["Origin Airport Code"] == selected_code]

                if not selected_row.empty:
                    row = selected_row.iloc[0]

                    st.sidebar.markdown(f"**Airport Name:** {row.get('airport_name', 'N/A')}")
                    st.sidebar.markdown("---")

                    # ✈️ FLIGHT ACTIVITY SUMMARY
                    st.sidebar.markdown("### ✈️ Flight Activity")
                    st.sidebar.markdown(f"**Total Departures:** {int(row.get('Total Departures', 0))}")
                    st.sidebar.markdown(f"**Total Flights Tracked:** {int(row.get('arr_flights', 0))}")
                    st.sidebar.markdown(f"**Cancellations:** {int(row.get('cancelled', 0))}")
                    st.sidebar.markdown(f"**Diversions:** {int(row.get('diverted', 0))}")
                    st.sidebar.markdown("---")

                    # 🕒 DELAY METRICS
                    st.sidebar.markdown("### 🕒 Delay Metrics")
                    st.sidebar.markdown(f"**Delayed Flights (>15 min):** {int(row.get('arr_del15', 0))}")
                    st.sidebar.markdown(f"**Carrier Delay (min):** {row.get('carrier_ct', 0):.2f}")
                    st.sidebar.markdown(f"**Weather Delay (min):** {row.get('weather_ct', 0):.2f}")
                    st.sidebar.markdown(f"**NAS Delay (min):** {row.get('nas_ct', 0):.2f}")
                    st.sidebar.markdown(f"**Security Delay (min):** {row.get('security_ct', 0):.2f}")
                    st.sidebar.markdown(f"**Late Aircraft Delay (min):** {row.get('late_aircraft_ct', 0):.2f}")
                    st.sidebar.markdown("---")

                    # 💸 COST INFO (optional to keep)
                    st.sidebar.markdown("### 💸 Fare Info")
                    st.sidebar.markdown(f"**Average Fare (2024):** ${row.get('average_fare', 0):.2f}")

                else:
                    st.sidebar.warning("No detailed data available for this airport.")
        else:
            st.warning("No airports found within the selected departure range.")


        
        # Slider uesed to be here, decided to apply it to the entire map
        
        
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        logging.error(f"Error fetching data: {e}")


# ------------------------------- This page will be a revenue and delay calculator -------------------------------
# The user will be able to select an airport code, number of passengers, and etc to calculate the amount of money
# that airport in the United States would make in a year (modeled after 2024 data)
# the computations are based on the Airlines for America data and statistics report for 2023 (unfortunately not 2024 yet)
# This report is available: https://www.airlines.org/dataset/u-s-passenger-carrier-delay-costs/#:~:text=In%202023%2C%20the%20average%20cost,percent%20to%20%2432.68%20per%20minute.
# It allows for the user to see how much a delay costs the airline

elif page == "Revenue & Delay Calculator - 2024 Data":
    st.title("FlyBuy - 📊 Revenue & Delay Impact Calculator")
    st.info("Now for the 'buy' in FlyBuy!")
    with st.expander("📘 Page Details:"):
        st.markdown("""
        This page helps you estimate potential revenue losses from delays at U.S. airports.
        
        **How it works:**
        - Select an airport.
        - Enter the expected number of passengers (annually or for one flight).
        - Based on historical data and industry averages, the app estimates the total cost impact of delays at that airport.

        **Cost Reference:**
        - Average cost per delayed flight: **$2,003.40**
        - Average passengers per flight: **150**
        - → Estimated cost per delayed passenger: **$13.36**
        """) # Had chaptgpt write the definitions (faster)
                
    # for this section, refer back to Fare_Delay data to get the specifics for each airport
    st.subheader("✈️ Choose Your Airport")
    Fare_Delay["airport"] = Fare_Delay["airport"].str.strip().str.upper()
    airport_codes = Fare_Delay["airport"].unique().tolist()

    # Create a selectbox for the user to choose an airport code
    selected_airport = st.selectbox("Select an Airport Code", airport_codes, index=0)

    st.subheader("👥 Passenger Amount")
    # will use a number input for the user to enter the number of passengers
    passenger_amount = st.number_input(
         "Enter the expected number of passengers (annually or for one flight, e.g., 100 for a flight, 10000 for a year)",
            min_value=1,
            step=1,
    )
    
    # from Airlines for America, the average cost per delayed flight is $2,003.40
    # Per passenger, the cost is $13.36
    cost_per_delayed_flight = 2003.40
    cost_per_delayed_passenger = 13.36

    airport_data = Fare_Delay[Fare_Delay["airport"] == selected_airport]

    if not airport_data.empty:
         row = airport_data.iloc[0]
         delay_rate = row.get("arr_del15", 0) / row.get("arr_flights", 1) * 100 # as a percentage
         delayed_passengers = passenger_amount * (delay_rate / 100) # number of delayed passengers
         not_delayed_passengers = passenger_amount - delayed_passengers # number of not delayed passengers
         delaycost = delayed_passengers * cost_per_delayed_passenger # cost of delay
         avg_fare = row.get("average_fare", 0) # average fare cost
         gross_revenue = passenger_amount * avg_fare # gross revenue from passengers
         net_revenue = gross_revenue - delaycost

         st.markdown("---")
         st.subheader("📉 Estimated Delay Cost Impact")

         st.metric("Delay Rate (%)", f"{delay_rate:.2f}%")
         st.metric("Estimated Delayed Passengers", f"{delayed_passengers:,.0f}")
         st.metric("Total Estimated Cost of Delays", f"${delaycost:,.2f}")
         st.metric("Gross Revenue (No Delays)", f"${gross_revenue:,.2f}")
         st.metric("Adjusted Revenue (Post-Delay)", f"${net_revenue:,.2f}")
         

         st.caption(f"Based on ${cost_per_delayed_passenger} per delayed passenger & average fare of ${avg_fare:.2f} at {selected_airport}.")
         
    else:
         st.warning("No data available for the selected airport.")


    # ------------------------------------- This is the final portion of the code -------------------------------------
    # On this final page I decided to add a sankey diagram to show how the delays effect the airline revenue
    # I decided plotly would be the best option for this, more user friendly and interactive
    # Highlight the chosen airport path for clear user chosen analysis compared to the rest of the airports

    # Originally I focused on delays as a whole, the diagram was lack luster and the data already had different delay types
    # Wonderful opportunity to combine their likelihoods into this sort of diagram

    # Delay Seperation via row.get
    carrier = row.get("carrier_ct", 0)
    weather = row.get("weather_ct", 0)
    security = row.get("security_ct", 0)
    late = row.get("late_aircraft_ct", 0)
    nas = row.get("nas_ct", 0)

    delay_total = carrier + weather + security + late + nas
    
    # Original data makes it difficult to read the sankey data, will implement an amplifier for it to be easier to read
    amplifier = 20

    delay_section_map = {
         "Carrier Delay": carrier,
         "Weather Delay": weather,
         "Security Delay": security,
         "Late Aircraft Delay": late,
         "NAS Delay": nas
    }

    labels = [
         f"{selected_airport} Passengers",
         "On Time Passengers",
         "Delayed Passengers",
         "Carrier Delay",
         "Weather Delay",
         "Security Delay",
         "Late Aircraft Delay",
         "NAS Delay",
         "Gross Revenue",
         "Delay Cost",
         "Net Revenue",
    ]
    
    # Enumerate to create indices for labels
    label_indices = {label: i for i, label in enumerate(labels)} # didnt know you could make a for loop like this, very fun


    # Initialize Lists
    sources = [] # The beginning of a flow
    targets = [] # The end of a flow
    values = [] # The values that determines the flow
    colors = []

   
    # Originally labeled sources individually, inefficient
    sources += [label_indices[f"{selected_airport} Passengers"]] * 2
    targets += [label_indices["Delayed Passengers"], label_indices["On Time Passengers"]]
    values += [delayed_passengers, not_delayed_passengers]
    colors += ["#c6dbef", "#9ecae1"]

    # Sankey diagrams work in flows so much construct the direction the flows go in

    # Delayed Passenger -> Delay Causes
    for delay_type, minutes in delay_section_map.items():
        if delay_total > 0:
            share = minutes / delay_total
            delay_passengers = share * delayed_passengers
            sources.append(label_indices["Delayed Passengers"])
            targets.append(label_indices[delay_type])
            values.append(delay_passengers * amplifier) # THICK - Without this the mass amount of revenue makes the delays seem small, had to thicken lines for better representation
            colors.append("#6baed6") 

            
            sources.append(label_indices[delay_type])
            targets.append(label_indices["Delay Cost"])
            values.append((delay_passengers * cost_per_delayed_passenger) * amplifier)
            colors.append("#084594")

            # Note, had Chatgpt help with format, I originally had delay and passenger constribution have the same weight
            # This did provide the data storytelling I wanted, reformatting was simpler this way but I understand the flow
            # Principle of the sankey diagram and the append process

   

    # On-time -> Gross revenue
    sources.append(label_indices["On Time Passengers"])
    targets.append(label_indices["Gross Revenue"])
    values.append(not_delayed_passengers * avg_fare)
    

    # Delayed -> Gross Revenue - Tickets are still sold and oftentimes nto refunded
    sources.append(label_indices["Delayed Passengers"])
    targets.append(label_indices["Gross Revenue"])
    values.append(delayed_passengers * avg_fare)
    

    # Gross Revenue combined with the delay costs produces the net revenue
    sources += [label_indices["Gross Revenue"], label_indices["Delay Cost"]]
    targets += [label_indices["Net Revenue"], label_indices["Net Revenue"]]
    values += [gross_revenue, delaycost]
    colors += [
        "#4292c6",  # On-Time → Gross Revenue
        "#6baed6",  # Delayed → Gross Revenue
        "#2171b5", "#084594"  # Gross + Cost → Net
    ]
                   

    ## Proof of concept before constructing a more complicated plot ##
    ## May ignore other than for simple reference ##

    # Need to create indices that align witht the labels created - according to plotly
    # sources = [0, 0, 1, 2, 3, 4]
    # targets = [1, 2, 3, 4, 5, 5]

    # highlight_color = "blue"  # Color for the selected airport path

    # values = [
         # not_delayed_passengers, # On Time Passengers
         # delayed_passengers, # Delayed Passengers
         # not_delayed_passengers * avg_fare, 
         # delaycost, # Delay Cos
         # gross_revenue, # Gross Revenue
         # delaycost, # 
    #]
    # Color labels for highlighting
    #node_colors = [highlight_color] + ["darkblue"] * (len(labels) - 1)
    #link_colors = [highlight_color] + ["lightgray"] * (len(sources) - 1)

    # Create figure
    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            pad=20,
            thickness=24,
            line=dict(color="white", width=0.5),
            label=labels,
            color="#f0f8ff",
            hovertemplate="%{label}<extra></extra>" # I have to say, love the hover capabilities
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=colors,
            hovertemplate="%{value:,.0f} passengers / $%{value:,.0f} cost<extra></extra>"
        )
    )])

    fig.update_layout(
        font=dict(family="Segoe UI", size=14),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(t=20, b=20, l=20, r=20)
    )

    st.subheader("Delay Impact Sankey Diagram")
    st.plotly_chart(fig, use_container_width=True)

