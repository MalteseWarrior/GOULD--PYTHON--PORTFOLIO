## Instructions for terminal:
# cd basic-streamlit-app
# run streamlit OR python -m streamlit run main.py

# Libraries
import streamlit as st

import pandas as pd

import time

import matplotlib.pyplot as plt

import math

# App Introduction Creation
Welcome_Message = "Welcome, This is Ginger's"

def entry_message():
    for word in Welcome_Message.split(" "):
        yield word + " "
        time.sleep(0.3)
    
st.write_stream(entry_message)

st.title("Basic Streamlit App")


Description_Message = ("This is a basic app created using streamlit for Python! "
                       "This app provides an analysis of casino data provided by "
                       "the University of Las Vegas (UNLV). The data spans from "
                       "the years 2000 - 2022 and includes data of specific casino "
                       "revenue generation and how it has changed throughout the years.")

def description_message():
    for word in Description_Message.split(" "):
        yield word + " "
        time.sleep(0.1)
st.write_stream(description_message)

# Create toggle frame for description of variables
with st.expander("Definitions:"):
    st.text("Units: Total number of sports betting locations active during the calendar year"
    "\nWin Amount: Cash-in minus payoffs; the amount the sports books kept for the calendar year"
    "\n% Change: Percentage change in win from the previous year"
    "\nWin%: Win percentage, or win as a percentage of drop, AKA hold percentage, the percentage of money wagered that the casino kept"\
    "\nDrop: Estimated total amount bet by bettors during the calendar year, derived by dividing the Win by the Win Percentage"\
    "\nTotal Gaming Win: Total amount won by casinos on all games and devices during the calendar year"
    "\n% Total: Sports betting win as a percentage of total casino win"
    "\nWin/Unit: Average win per unit for the calendar year")

# Implement Casino UNLV_Casino_Data.csv
st.header("Casino Games & Revenue Progression")
casinodata = pd.read_csv("./data/UNLV_Casino_Data.csv")


st.dataframe(casinodata)

# Filtering Options, user interactivity :D
st.subheader("Select how you want to visualize the data!")

# First Option
gametype1 = st.selectbox(
    "Select the first game type you want to compare data with",
    ("Slot Machines", "Table Games", "BlackJack", "Baccarat", "Craps", "Sports Book"),
)

# Second Option
gametype2 = st.selectbox(
    "Select the second game type you want to compare data with",
    ("Slot Machines", "Table Games", "BlackJack", "Baccarat", "Craps", "Sports Book"),
)

# Third Option
datatype = st.selectbox(
    "Now, what variable do you want to see with that game type?",
    ("Units", "Win Amount", "WPU", "WUD", "Win%")
)

Done = st.button("Press when done selecting data!")

# Display Data in Chart Form
if Done:
    GameType = "GameType"
    
    # Filter the data for the selected game types
    filtered_data1 = casinodata[casinodata[GameType] == gametype1]
    filtered_data2 = casinodata[casinodata[GameType] == gametype2]

    # Create a figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot lines for data
    ax.plot(filtered_data1["Year"], filtered_data1[datatype], color="blue", label=gametype1)
    ax.plot(filtered_data2["Year"], filtered_data2[datatype], color="red", label=gametype2, alpha=0.7)

    # Labels and title
    ax.set_xlabel("Year")
    ax.set_ylabel(datatype)
    ax.set_title(f"Comparison of {gametype1} vs {gametype2}")
    ax.legend()

    # Display in Streamlit
    st.pyplot(fig)

    # Balloons for fun, I like this function
    st.balloons()


st.text("References"
"\nLibraries, U. U. (n.d.). Reports, Data Sets, & Research Guides. UNLV University Libraries Center for Gaming Research - All Reports. https://gaming.library.unlv.edu/all-reports.html")