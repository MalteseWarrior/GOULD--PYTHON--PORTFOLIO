# ✈️ FlyBuy - Real-Time Flight Data & U.S. Airport Analysis ![flying_airplane](https://github.com/user-attachments/assets/e66000c3-f66f-49f0-8803-e0fb39e5c408)




# Welcome!
This is a streamlit Python application that allows you to search for flights in real time using the OpenSky API.  
Along with the flight data, it also provides details about the airports in the United States as it is the origin country with the most  
departure flights BY FAR. With this, the location and total flight departures relative to airport codes are displayed in both a bar chart and a proportional map.  
With this, flight delay data was combined with average fare per airport to construct a quick and interactive analysis on how much revenue an airport generates with respect to 2024 Bureau of Transportation data.  
The user is given the opportunity to analyze the average fare cost of the flight, and the amount delays actually cost an airport relative to the fare price.  
In other words, this app was created to recognize flight departure patterns and how much different delays impact the final revenue of an airport in the country with the largest departure flights in the world: the United States. Delayed flights can be annoying, but with this application's
analysis it becomes apparent its only really annoying for the delayed passenger.

---

## 🚀 How to Use

### ▶️ Access the App on Streamlit
You can access this application on the Streamlit Community Page:  
**[FlyBuy](https://flybuy.streamlit.app/)**

Or run it locally, instructions below

### Page 1:
- Presents a pydeck map that displays live flight data by call sign and country of origin  
- Presents a live number of the number of active departures in the world  
- The User may specify the country of origin for analysis - Sometimes you need to do it twice... I dont know why  
- A Plotly bar chart is provided for active comparison between countries

  ![image](https://github.com/user-attachments/assets/0bbd8b5e-942c-40a0-88f8-c95e1f046eff)


### Page 2:
- Presents a proportional plot map using Pydeck to visualize 2024 airport data in the United States  
- Emphasizes airports relative to their total flight departures annually  
- The user may use a slider to go between the minimum and maximum flight departures in the data to see which airports fit in that range  
- The sidebar provides extra information that alludes to the third page, as it gives information on the selected airport's delays and average fare  

![image](https://github.com/user-attachments/assets/bd94914a-401e-4bb7-9cd2-6d1c7fa0fa9a)


### Page 3:
- A user-friendly calculator that allows the user to see how much delays will cost a respective airport per delayed passenger  
- The numbers were calculated with industry standards (it costs approximately $13 per delayed passenger)  
- The amount of money lost is approximated using the delay likelihood at the selected airport  
- For a visualization of the relationship between total passengers, delayed passengers, gross revenue, and net revenue, a Sankey diagram was constructed  
- Sankey diagram is an attempt to visualize the contribution of delays to the net revenue - interestingly, they contribute little despite high fares  

![image](https://github.com/user-attachments/assets/758a8aeb-9c5c-4c63-8cf9-e2f6f8b84196)

---


## SPECIAL THANKS

Special thanks to these websites and organizations for their help in constructing this app:  
- [Geeksforgeeks](https://www.geeksforgeeks.org/)
- [Pydeck](https://deckgl.readthedocs.io/en/latest/deck.html)  
- [Pydeck (again)](https://deckgl.readthedocs.io/en/latest/gallery/scatterplot_layer.html)  
- [Plotly](https://plotly.com/python/sankey-diagram/)  
- [Plotly (again)](https://plotly.com/python/bar-charts/)  
- [Streamlit Documentation (I love this website)](https://docs.streamlit.io/)  
- ChatGPT: The app would not look this good without it (Which means I need to learn CSS at some point)  

And of course, thank you to Professor Smiley, who helped me learn so much more about python and data analysis.  
I greatly appreciate the opportunities he provided me to expand my knowledge in this space, even when my ideas were too above and beyond at times.  

---

## Data Allocation

The Data used in this project was sourced from a few different websites and organizations such as:
- [Bureau of Transportation](https://www.bts.gov/)
- [OpenDataSoft](https://www.opendatasoft.com/en/)
- [OpenSky API](https://opensky-network.org/data/api)
- [Airlines for America](https://www.airlines.org/dataset/u-s-passenger-carrier-delay-costs/)
  

---

## Running FlyBuy Locally - Library install and streamlit run

Install all relevant files in the repository, including the main file, FlyBuy.py
and the associated data files. It is easiest to download the inter StreamlitAppFinal folder

Before running the code, make sure you have the required libraries installed. Especially if you are using a virtual environment.  
This is a warning for all you local users out there. If you are using the Streamlit community cloud, you can ignore this. 

If in an Anaconda environment (what I use), you can activate your environment in Anaconda Prompt and then write:

```bash
pip install streamlit
pip install pandas
pip install numpy
pip install pydeck
pip install plotly
pip install streamlit-plotly-events
pip install requests


# Then in your terminal:
# Use the 'cd' command to navigate to the folder where FlyBuy.py and its data files are located
cd path/to/your/project

# Finally, launch the app with:
streamlit run FlyBuy.py
