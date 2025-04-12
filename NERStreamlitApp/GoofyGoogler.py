## Welcome to the GoofyGoogler! This a SpongeBob Squarepants themed Name Entityy Regcognition (NER) application
## This application uses spaCy and Streamlit to extract named entities from text and display them in a fun and interactive way.
## This application is designed to be a fun and engaging way to learn about named entity recognition and the characters from SpongeBob Squarepants.

# To laucnh
# cd NERStreamlitApp
# dtreamlit run GoofyGoogler.py OR python -m streamlit run GoofyGoogler.py

## Import Libraries
import streamlit as st
import spacy
import pandas as pd
import numpy as np


## ---------- Load Data From GoofyScraper.py ---------- ##
SpongeData = pd.read_csv('spongebob_transcripts.csv')


## ---------- Load the spaCy model for named entity recognition ---------- ##
## ---------- Create Patterns for NER ---------- ##

nlp = spacy.load("en_core_web_sm")

# The dataframe is structured as follows:
# Column 1: Episode Name
# Column 2: Character Name
# Column 3: Character Dialogue
# Because of this the patterns will be based on this structure and through a for loop to capture every character and their dialogue

chapatterns = []
for i in range(len(SpongeData)):
    chapatterns.append({"label": SpongeData.iloc[i, 1], "pattern": SpongeData.iloc[i, 2]})

dialogpatterns = []
for i in range(len(SpongeData)):
    dialogpatterns.append({"label": SpongeData.iloc[i, 2], "pattern": SpongeData.iloc[i, 1]})

print(chapatterns)
print(dialogpatterns)
    
