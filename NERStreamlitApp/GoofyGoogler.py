## Welcome to the GoofyGoogler! This a SpongeBob Squarepants themed Name Entityy Regcognition (NER) application
## This application uses spaCy and Streamlit to extract named entities from text and display them in a fun and interactive way.
## This application is designed to be a fun and engaging way to learn about named entity recognition and the characters from SpongeBob Squarepants.

## Also, since I wanted to expand my knowledge of transformers and language models I have implemented
## Transformers into this application, but the majority is manual input other than episode descriptiona and recognition

# To laucnh
# cd NERStreamlitApp
# dtreamlit run GoofyGoogler.py OR python -m streamlit run GoofyGoogler.py

## Import Libraries
import streamlit as st
import spacy
import pandas as pd
import numpy as np
from collections import defaultdict
from spacy.pipeline import EntityRuler
import re
from collections import Counter
import random
import os
# Considering transformers, since I have a large data set I thought converting them into
# vectors and through the cosine similarity I could compile it all to create a unique 
# experience for every user - this is my first time working with transformers and a lot of this
# is taking from the internet and ChatGPT so I dont break anything (which still happened...alot), but I had fun learning
# the most from this project and I am excited to learn more about transformers and language models in the future
from sentence_transformers import SentenceTransformer, util
from sentence_transformers.util import cos_sim


## ---------- Load Data From GoofyScraper.py ---------- ##
# After some research to make this more efficient a function would be best to just load the data set
csv_path = os.path.join(os.path.dirname(__file__), "spongebob_transcripts.csv") # For local, change to just read_csv
SpongeData = pd.read_csv(csv_path)


# Drop bad rows before any filtering logic
SpongeData.dropna(subset=['ep', 'char', 'text'], inplace=True)

# Ensure all values are string before string methods are used
SpongeData['text'] = SpongeData['text'].astype(str)
SpongeData['char'] = SpongeData['char'].astype(str)
SpongeData['ep'] = SpongeData['ep'].astype(str)

# Now safely apply your filtering logic
long_enough = SpongeData['text'].str.len() > 10
not_junk = ~SpongeData['text'].str.contains("Season|shorts|Movie|Theme parks|Specials|Patchy", case=False, na=False)
valid_char_names = SpongeData['char'].str.count(" ") < 5

SpongeData = SpongeData[long_enough & not_junk & valid_char_names]


# Remove rows where any critical field is empty or whitespace
SpongeData = SpongeData[
    (SpongeData['ep'].str.strip() != "") &
    (SpongeData['char'].str.strip() != "") &
    (SpongeData['text'].str.strip() != "")
]

# Final type cast (optional but safe)
SpongeData = SpongeData.astype(str)


# Location data had to be defined beforehand to avoid long stringd
# I did it wrong the first time, it wasnt recognizing the locations with mutliple spacings
def location_token_patterns(location_list):
    patterns = []
    for loc in location_list:
        tokens = [{"LOWER": word.lower()} for word in loc.strip().split()]
        # Add flexible version with optional "the"
        if tokens[0]["LOWER"] != "the":
            tokens_with_the = [{"LOWER": "the"}] + tokens
            patterns.append({"label": "LOCATION", "pattern": tokens_with_the})
        patterns.append({"label": "LOCATION", "pattern": tokens})
    return patterns



# Created function for efficiency
def load_spacy_model():
    nlp = spacy.load("en_core_web_sm")
    ruler = nlp.add_pipe("entity_ruler", before="ner")

    # The dataframe is structured as follows:
    # Column 1: Episode Name
    # Column 2: Character Name
    # Column 3: Character Dialogue
    # Because of this the patterns will be based on this structure and through a for loop to capture every character and their dialogue
    patterns  = []

    # Episode
    for ep in SpongeData["ep"].unique():
        patterns.append({"label": "EPISODE", "pattern": ep})

    # Character - Dataframe lists some actions in character section, usually above 2 words
    # So event names will be filtered out and put into their own category
    
    for char in SpongeData["char"].unique():
        if len(char.split()) > 2:
            patterns.append({"label": "EVENT", "pattern": char})
        else:
            patterns.append({"label": "CHARACTER", "pattern": char})


    location_names = [
    "Krusty Krab", "The Krusty Krab", "Krusty Krab Pizza", "Chum Bucket", "Rock Bottom",
    "Goo Lagoon", "Jellyfish Fields", "Sandy's Treedome", "Mrs. Puff's Boating School",
    "Shell City", "Glove World", "The Salty Spitoon", "Bikini Bottom", "Karate Island",
    "The Flying Dutchman's Ship", "Bikini Bottom Hospital", "Bikini Bottom Library"]

    
    patterns.extend(location_token_patterns(location_names))
    
    
    ruler.add_patterns(patterns)
    return nlp

## ---------- Load the spaCy model for named entity recognition ---------- ##
## ---------- Create Patterns for NER ---------- ##

nlp = load_spacy_model()


## ---------- Create SentenceTransformer model for semantic similarity ---------- ##
@st.cache_resource(show_spinner=False) # Caching the model to avoid reloading it every time


# i originally just had the model, but I wanted to add the characters and episodes to the model
# chatgpt suggested semantic indexing - this is going to help the NER model find context within the text
# I didnt understand the .encode function at first, but it is used to convert the text into a numerical representation
# I had to have chatgpt edit my initial code because of performance issues and the fact that I was using a lot of memory



@st.cache_resource
def build_semantic_index(df):
    model = SentenceTransformer("all-MiniLM-L6-v2")

    # apparently the dialogue is not enough to classify characters, create character alias
    character_aliases = {
        "Spongebob" : ["SpongeBob", "Sponge Bob", "SpongeBob Squarepants", "yellow sponge", "patrick's best friend", "fry cook"],
        "Patrick" : ["Patrick Star", "pink starfish", "spongebob's best friend"],
        "Squidward" : ["Squidward Tentacles", "squidward", "squidward tentacles", "squid", "octopus", "cashier"],
        "Mr. Krabs" : ["Eugene Krabs", "Mr. Krabs", "krabby patty", "money", "krabby krab"],
        "Gary" : ["Gary the Snail", "snail", "spongebob's pet"],
        "Jellyfish" : ["jellyfish", "jelly fish", "sponge bob jellyfish"],
        "Kevin" : ["Kevin the Jellyfish", "Kevin", "jellyfish"],
        "Larry" : ["Larry the Lobster", "Larry", "lobster"],
        "Ms. Puff" : ["Ms. Puff", "puff", "boating school"],
        "Plankton" : ["Plankton", "chum bucket", "evil genius"],
        "Sandy" : ["Sandy Cheeks", "squirrel", "texas"],
        "Pearl" : ["Pearl Krabs", "pearl", "whale"],
        "Bubble Bass" : ["Bubble Bass", "bass", "krabby patty"],
        "Karen" : ["Karen Plankton", "computer wife", "plankton's wife"],
        "Poseidon" : ["Poseidon", "king of the sea"],
        "King Neptune" : ["King Neptune", "king of the sea"],
    }

    char_descriptions = []
    characters = []
    for c in df['char'].unique():
        lines = df[df['char'] == c]['text'].tolist()
        if len(lines) > 3:
            desc = ' '.join(lines[:3])
        else:
            desc = character_aliases.get(c, c)
        char_descriptions.append(desc)
        characters.append(c)


    episodes = df['ep'].unique().tolist()
    ep_descriptions = []
    for ep in episodes:
        lines = df[df['ep'].str.lower() == ep.lower()]['text'].tolist()
        filtered_lines = [
            line for line in lines
            if len(line.split()) > 3 and
               not any(x in line.lower() for x in ["season", "shorts", "patchy", "special", "theme park", "movie"])
        ]

        # Boost iconic lines containing keywords
        pizza_lines = [l for l in filtered_lines if "pizza" in l.lower()]
        if pizza_lines:
            sample = " ".join(pizza_lines[:3]) + " " + " ".join(filtered_lines[:12])
        else:
            sample = " ".join(filtered_lines[:15])

        ep_descriptions.append(sample)

    char_embeddings = model.encode(char_descriptions, convert_to_tensor=True)
    ep_embeddings = model.encode(ep_descriptions, convert_to_tensor=True)

    return {
        "model": model,
        "characters": characters,
        "char_embeddings": char_embeddings,
        "episodes": episodes,
        "ep_embeddings": ep_embeddings
    }




semantic_index = build_semantic_index(SpongeData)

## ---------- Function to find similar characters or episodes --------- ##  
def semantic_match(query, labels, embeddings, model, cutoff=0.3):
    query_embedding = model.encode(query, convert_to_tensor=True)
    scores = util.cos_sim(query_embedding, embeddings) # this is the cosine similarity function, not sure on the util
    best_idx = int(scores.argmax())
    best_score = float(scores[0][best_idx])
    return (labels[best_idx], best_score) if best_score >= cutoff else (None, best_score)

## ---------- UI Interface on Streamlit App ---------- ##
# This section prioitizes the UI interface of the Streamlit app and how it will be displayed to the user
# The app will have a title, a header, and a text input box for the user to enter their text and output the results associated with the NER
# The app will also have a button to run the NER and display the results in a table format
# The app will have the option to use their text to search for similar or related text in the dataset
# such as describing an event, a character, or a specific episode

# Load Gifs - Make sure to have downloaded the UIgraphics from the GitHub repository and place them in the same directory as this file
# Get the full directory path where this script is running
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GRAPHICS_DIR = os.path.join(BASE_DIR, "UIGraphics")


character_gifs = {
    "SpongeBob": "https://raw.githubusercontent.com/MalteseWarrior/GOULD--PYTHON--PORTFOLIO/main/NERStreamlitApp/UIGraphics/spongebob.gif",
    "Patrick": "https://raw.githubusercontent.com/MalteseWarrior/GOULD--PYTHON--PORTFOLIO/main/NERStreamlitApp/UIGraphics/patrick_dance.gif",
    "Squidward": "https://raw.githubusercontent.com/MalteseWarrior/GOULD--PYTHON--PORTFOLIO/main/NERStreamlitApp/UIGraphics/squidward.gif",
    "Mr. Krabs": "https://raw.githubusercontent.com/MalteseWarrior/GOULD--PYTHON--PORTFOLIO/main/NERStreamlitApp/UIGraphics/MrKrabsMoney.gif",
    "Gary": "https://raw.githubusercontent.com/MalteseWarrior/GOULD--PYTHON--PORTFOLIO/main/NERStreamlitApp/UIGraphics/gary-the-snail.gif",
    "Jellyfish": "https://raw.githubusercontent.com/MalteseWarrior/GOULD--PYTHON--PORTFOLIO/main/NERStreamlitApp/UIGraphics/jellyfish.gif"
}





# Create summary templates for variety in sidebar
# provide a list of templates for main characters
# This is more for fuzzy matches
auto_summary_templates = [
    "{name} seems to really enjoy talking about {w1}, {w2}, and {w3}.",
    "{name} might be obsessed with {w1}, always mentioning {w2} and even {w3}.",
    "{name} is known for their love of {w1}, plus a lot of chatter about {w2} and {w3}.",
    "When {name} speaks, you’ll hear about {w1}, {w2}, and {w3} a lot!",
    "You can tell {name} really cares about {w1}, maybe even more than {w2} or {w3}.",
    "{name} has a knack for bringing up {w1}, and they often throw in {w2} and {w3} too.",
    "{name} is so interesting! They often talk about {w1}, and you can’t miss their mentions of {w2} and {w3}.",
]

character_bios = {
    "SpongeBob": "SpongeBob is a cheerful and optimistic sea sponge who works at the Krusty Krab.",
    "Patrick": "Patrick is SpongeBob's best friend, known for his goofy and carefree attitude.",
    "Squidward": "Squidward is SpongeBob's neighbor, often annoyed by SpongeBob's antics.",
    "Mr. Krabs": "Mr. Krabs is the greedy owner of the Krusty Krab, obsessed with money.",
    "Gary": "Gary is SpongeBob's pet snail who meows like a cat.",
    "Jellyfish": "Jellyfish are creatures in Bikini Bottom that SpongeBob and Patrick love to catch.",
    "Kevin": "Kevin is a character from the episode 'The Secret Box' who is known for his love of jellyfishing.",
    "Larry": "Larry is a lifeguard and fitness enthusiast in Bikini Bottom, known for his muscular physique.",
    "Ms. Puff": "Ms. Puff is SpongeBob's boating school teacher, often frustrated with his driving skills.",
    "Plankton": "Plankton is the owner of the Chum Bucket and always tries to steal the Krabby Patty secret formula.",
    "Sandy": "Sandy is a squirrel from Texas who lives underwater and is known for her intelligence and karate skills.",
    "Pearl": "Pearl is Mr. Krabs' teenage daughter, a whale who loves shopping and is often seen with her friends.",
    "Bubble Bass": "Bubble Bass is a recurring character known for his rivalry with SpongeBob and his love for Krabby Patties.",
    "Karen": "Karen is Plankton's computer wife, known for her sarcastic and witty remarks.",
    "Poseidon": "Poseidon is the king of the sea and a character from the episode 'The Sponge Who Could Fly.'",
    "King Neptune": "King Neptune is the ruler of the sea and a character from various episodes.",

}
# As a note, I want to add more characters to the character_bios dictionary in the future to make it more robust and fun for the user
# maybe add openAI?

# Original synopsis generation was slow and depended on stop words,this allows for unique words
# to be used in the summary and allows for a more accurate summary of the character
def get_global_word_counts(df):
    all_text = ' '.join(df['text'].str.lower().tolist())
    words = re.findall(r'\b\w{4,}\b', all_text)
    return Counter(words)

# Create function for synopsis generation - I wanted to play around with sentiment analysis and learn more about it
# This function was created with the help of stackoverflow and ChatGPT for clarity and efficiency
# Learned about lemmatization, simplifies words to their base form so "running" becomes "run"
global_word_counts = get_global_word_counts(SpongeData)

def generate_synopsis(character_name, df, max_lines=200):
    
    for known_name in character_bios:
        if known_name.lower() in character_name.lower():
            char_lines = df[df['char'].str.lower() == character_name.lower()]['text'].tolist()
            quote = f'"{char_lines[0]}"' if char_lines else "🤷‍♂️ No quote available."

            return {
                "Character": character_name,
                "Lines": len(char_lines),
                "Summary": character_bios[known_name],
                "Sample Quote": quote
            }

    char_lines = df[df['char'].str.lower() == character_name.lower()]['text'].tolist()

    if not char_lines:
        return {
            "Character": character_name,
            "Lines": 0,
            "Summary": "No dialogue found. But they're probably still goofy!",
            "Sample Quote": "🤷‍♂️ No quote available."
        }

    char_lines = char_lines[:max_lines]
    all_text = ' '.join(char_lines).lower()

    # The lemmatization process is used to reduce words to their base form
    doc = nlp(all_text)
    lemmas = [
        token.lemma_.lower()
        for token in doc
        if token.is_alpha and len(token) >= 4 and not token.is_stop
    ]

    word_counts = Counter(lemmas)
    filtered_word_counts = {
        word: count for word, count in word_counts.items()
        if global_word_counts.get(word, 0) > 3
    }

    unique_scores = {
        word: count / global_word_counts.get(word, 1)
        for word, count in filtered_word_counts.items()
    }

    top_keywords = sorted(unique_scores.items(), key=lambda x: x[1], reverse=True)[:5]
    top_words = [word for word, _ in top_keywords]

    # 🎨 Use friendly template if we have enough words
    if len(top_words) >= 3:
        w1, w2, w3 = top_words[:3]
        template = random.choice(auto_summary_templates)
        summary = template.format(name=character_name, w1=w1, w2=w2, w3=w3)
    else:
        summary = f"{character_name} has a mysterious vibe... not much is known."

    return {
        "Character": character_name,
        "Lines": len(char_lines),
        "Summary": summary,
        "Sample Quote": f'"{char_lines[0]}"'
    }


# For clarity, I had ChatGPT assist me with the CSS styling as I am not familiar with CSS and HTML (yet)
# I did this because chatgpt is quick in finding the links for the fonts and colors, I knew the base functions
# such as st.sidebar, st.markdown, st.textarea, st.button, but I knew what I wanted visually would be faster with chatgpt
# ---------- STYLED TITLE & SUBTITLE ---------- #
st.markdown("""
    <style>
    @import url("https://fonts.googleapis.com/css2?family=Bubblegum+Sans&display=swap");

    .bubble-title {
        font-family: 'Bubblegum Sans', cursive;
        font-size: 48px;
        text-align: center;
        color: #ff69b4;
        background-color: #fff0fa;
        padding: 20px;
        border: 4px dotted #ffb6c1;
        border-radius: 25px;
        margin-bottom: 10px;
        box-shadow: 0 4px 8px rgba(255, 105, 180, 0.2);
    }

    .subtitle {
        font-family: 'Bubblegum Sans', cursive;
        font-size: 20px;
        text-align: center;
        color: #6c6cff;
        margin-bottom: 30px;
    }
    </style>

    <div class="bubble-title">GoofyGoogler</div>
    <div class="subtitle">A SpongeBob SquarePants NER App full of nautical nonsense 🫧</div>
""", unsafe_allow_html=True)



# ---------- Text Field ---------- #
user_input = st.text_area("🎤 Enter your Bikini Bottom text:", height=200, placeholder="Type Something Worthy of The Krabby Kronicle...")

# ---------- Analysis will begin at the push of a button ---------- #
if st.button("🎣 Go Fish!"):
    if user_input:
        doc = nlp(user_input)
        found_characters = set(ent.text for ent in doc.ents if ent.label_ == "CHARACTER")
        found_episodes = set(ent.text for ent in doc.ents if ent.label_ == "EPISODE")
        found_dialogues = set(ent.text for ent in doc.ents if ent.label_ == "DIALOGUE")
        found_locations = set(ent.text for ent in doc.ents if ent.label_ == "LOCATION")
        found_events = set(ent.text for ent in doc.ents if ent.label_ == "EVENT")

        # Episode cards
        def render_episode_cards(episode_names, df):
            if not episode_names:
                return

            st.markdown("""
                <style>
                .episode-gallery {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                    justify-content: center;
                }

                .episode-card {
                    background: linear-gradient(to bottom right, #fff0fa, #e0f7ff);
                    border: 4px dotted #ffb6c1;
                    border-radius: 20px;
                    width: 300px;
                    padding: 1rem;
                    box-shadow: 2px 4px 12px rgba(255, 105, 180, 0.2);
                    font-family: 'Bubblegum Sans', cursive;
                }

                .episode-title {
                    font-size: 24px;
                    color: #ff69b4;
                    margin-bottom: 0.5rem;
                }

                .episode-meta {
                    font-size: 14px;
                    color: #6c6cff;
                    margin-bottom: 0.6rem;
                }

                .episode-line {
                    font-style: italic;
                    color: #333;
                    font-size: 14px;
                }
                </style>
            """, unsafe_allow_html=True)

            st.markdown("## 📺 Possible Episodes")
            st.markdown('<div class="episode-gallery">', unsafe_allow_html=True)

            for ep in episode_names:
                ep_data = df[
                    (df['ep'].str.strip().str.lower() == ep.strip().lower()) &
                    (df['char'].str.strip().str.lower().isin([c.strip().lower() for c in found_characters]))]


                if ep_data.empty:
                    continue

                dialogue_lines = ep_data[
                    ep_data['text'].str.count(" ") > 3 &
                    ~ep_data['text'].str.contains("Season|shorts|Movie|Theme parks|Patchy", case=False, na=False)
                ]

                sample_line = dialogue_lines['text'].sample(1).values[0] if not dialogue_lines.empty else ""

                sample_chars = ', '.join(ep_data['char'].unique()[:4])

                card_html = f"""
                    <div class="episode-card">
                        <div class="episode-title">📀 {ep}</div>
                        <div class="episode-meta">👥 Featuring: {sample_chars}</div>
                        <div class="episode-line">💬 "{sample_line}"</div>
                    </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            for ep in episode_names:
                with st.expander(f"🧾 Show all dialogue from '{ep}'"):
                    ep_data = df[df['ep'].str.lower() == ep.lower()]
                    for _, row in ep_data.iterrows():
                        st.markdown(f"<b>{row['char']}:</b> {row['text']}", unsafe_allow_html=True)
    

        # Always try to enrich characters with fuzzy matching
        for _ in range(3):
            guessed_char, score = semantic_match(
                user_input,
                semantic_index["characters"],
                semantic_index["char_embeddings"],
                semantic_index["model"]
            )
            if guessed_char and guessed_char not in found_characters:
                found_characters.add(guessed_char)
                st.markdown(f"Sounds like you're talking about: **{guessed_char}** (confidence: {score:.2f})")

        # Always try to enrich episodes too
        guessed_ep, ep_score = semantic_match(
            user_input,
            semantic_index["episodes"],
            semantic_index["ep_embeddings"],
            semantic_index["model"]
        )
        if guessed_ep and guessed_ep not in found_episodes:
            found_episodes.add(guessed_ep)
            st.markdown(f"🎞️ Sounds like you're talking about: **{guessed_ep}** (confidence: {ep_score:.2f})")
            



        render_episode_cards(found_episodes, SpongeData)

        # --------- CUTE ENTITY TABLE CSS --------- #
        st.markdown("""
            <style>
            .entity-table {
                width: 100%;
                border-collapse: collapse;
                font-family: 'Bubblegum Sans', cursive;
                margin: 20px 0;
                background-color: #f0f8ff;
                border-radius: 15px;
                overflow: hidden;
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            }

            .entity-table th {
                background-color: #ffb6c1;
                color: #003366;
                padding: 12px;
                text-align: left;
            }

            .entity-table td {
                padding: 10px;
                border-top: 1px solid #e0e0e0;
                background-color: #e6f7ff;
                color: #003366;
            }

            .entity-table tr:hover {
                background-color: #d0f0ff;
            }
            </style>
        """, unsafe_allow_html=True)
        

        # --------- RENDER AS A PRETTY TABLE --------- #
        def render_entity_table(characters, episodes, dialogues, locations, events):
            entity_data = {
                "Entity Type": [],
                "Name": []
            }

            for char in sorted(characters):
                entity_data["Entity Type"].append("Character")
                entity_data["Name"].append(char)

            for ep in sorted(episodes):
                entity_data["Entity Type"].append("Episode")
                entity_data["Name"].append(ep)

            for line in sorted(dialogues):
                entity_data["Entity Type"].append("Dialogue")
                entity_data["Name"].append(line)

            for loc in sorted(locations):
                entity_data["Entity Type"].append("Location")
                entity_data["Name"].append(loc)

            for event in sorted(events):
                entity_data["Entity Type"].append("Event")
                entity_data["Name"].append(event)

                

            entity_df = pd.DataFrame(entity_data)

            table_html = entity_df.to_html(classes="entity-table", index=False, escape=False)
            st.markdown("### 🧽 Found the following entities:")
            st.markdown(table_html, unsafe_allow_html=True)

        
        render_entity_table(found_characters, found_episodes, found_dialogues, found_locations, found_events)
        


        # Display gifs in main app - kind of big
        for character in found_characters:
            for name, gif_path in character_gifs.items():
                if name.lower() in character.lower():
                    st.image(gif_path, caption=name, use_container_width=True)
                    break

        # Side bar for character summaries
        # ---------- SIDEBAR STYLING ---------- #
        st.markdown("""
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Bubblegum+Sans&display=swap');

            [data-testid="stSidebar"] {
                background-color: #d3eaff; /* ocean blue */
                padding: 1rem;
            }

            .sidebar-title {
                font-family: 'Bubblegum Sans', cursive;
                font-size: 28px;
                color: #ff8fc9; /* jellyfish pink */
                text-align: center;
                margin-bottom: 1rem;
            }

            .character-card {
                background-color: #fce4ff;
                border: 2px solid #ff8fc9;
                border-radius: 15px;
                padding: 1rem;
                margin-bottom: 1rem;
                font-family: 'Bubblegum Sans', cursive;
                color: #003366;
            }

            .character-card h3 {
                margin-top: 0;
                color: #ff69b4;
                font-size: 20px;
            }

            .character-gif {
                display: block;
                margin: 0 auto 10px auto;
                border-radius: 10px;
            }
            </style>
        """, unsafe_allow_html=True)
        # Sidebar title     
        st.sidebar.markdown('<h2 class="sidebar-title">🪝 What You Caught in the Net</h2>', unsafe_allow_html=True)

        for character in found_characters:
            summary = generate_synopsis(character, SpongeData)
            
            gif_path = None
            for name, path in character_gifs.items():
                if name.lower() in character.lower():
                    gif_path = path
                    break

            card_html = f'<div class="character-card"><h3>{summary["Character"]}</h3>'
        
            card_html += f"""
                <p>🧾 <b>Lines in Data:</b> {summary['Lines']}</p>
                <p>💬 <b>Sample:</b> {summary['Sample Quote']}</p>
             <p>🧠 <b>Summary:</b> {summary['Summary']}</p>
            </div>
            """
            st.sidebar.markdown(card_html, unsafe_allow_html=True)
        
        


