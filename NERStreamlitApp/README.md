# 🧽 GoofyGoogler: A SpongeBob SquarePants NER App

This application was developed to learn more about Name Entity Recognition (NER) as part of spaCy’s language model. To do this, a large dataset was created by scraping the internet for SpongeBob SquarePants-related episodes, character names, and dialogue (This is found in the `GoofyScraper.py`). Once this data was collected, it was converted into a csv for easy loading. The actual NER section of the application is simple, as names, episodes, events, and locations are derived from the located transcripts.

As an add-on to this project, there is an incorporation of transformers, sentiment analysis, and fuzzy association. This was in an attempt to learn more about vectorization and confidence-based generation.

As a note, this application is specifically for locating SpongeBob-related words and statements, so please keep that in mind when inputting your text for analysis! Also, the visuals look the best when not in dark-mode.

---

## 🚀 How to Use

### ▶️ Access the App on Streamlit
You can access this application on the Streamlit Community Page:  
**https://goofygooglr.streamlit.app/**

<img width="1198" alt="image" src="https://github.com/user-attachments/assets/65db3e6e-1d4e-4c08-a6f0-fd4eeb639067" />


### 🖥 Or Run It Locally

1. Run your python environment prompt (mine is anaconda)

2. Install the following libraries by using `pip install` or `conda install`:

   - Streamlit  
   - Spacy  
   - Pandas  
   - Numpy  
   - Defaultdic  
   - Counter  
   - Random  
   - SentenceTransformer  

3. If you are running locally, open the `GoofyGoogler.py` file and use the `cd` command to open the file location, then type:

   ```bash
   streamlit run GoofyGoogler.py
4. For local, you will also need to edit the initial load data command, it has been commented for reference
