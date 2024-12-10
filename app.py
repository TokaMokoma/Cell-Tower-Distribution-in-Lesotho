
import pandas as pd
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import folium
import streamlit as st
from streamlit_folium import folium_static


place_name = "Lesotho"
place_boundaries = ox.geocode_to_gdf(place_name)

# Ploting the base map of Lesotho
base = place_boundaries.plot(color='lightgray', edgecolor='black',figsize=(13, 13))

# # Loading the CSV file for Africa towers data
# africaTowersPath = 'Africa towers.csv'
# df = pd.read_csv(africaTowersPath)


# Filtering data for Lesotho cell Towers from African Cell Towers (not included in the code due to git hub file space limit)
filtered_df =pd.read_csv('LesothoCellTowersData.csv') 
filtered_df.to_csv('LesothoCellTowersData.csv', index=False)

# Creating geometry for towers using latitude and longitude
geometry = [Point(xy) for xy in zip(filtered_df['LON'], filtered_df['LAT'])]

# Converting the filtered dataframe into a GeoDataFrame with the geometry column
towereLocation = gpd.GeoDataFrame(filtered_df, geometry=geometry,crs="EPSG:4326")

# creating a folium map
m= folium.Map(location=[-29.299021,27.455681], zoom_start=7)  # Lesotho coordinates
# changing through different maps

# Add tile layers
# Add tile layers with attribution
tiles = {
    "OpenStreetMap": {
        "tile": "OpenStreetMap",
        "attribution": "Map data © OpenStreetMap contributors"
    },
    "Stamen Terrain": {
        "tile": "Stamen Terrain",
        "attribution": "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    },
    "Stamen Toner": {
        "tile": "Stamen Toner",
        "attribution": "Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL."
    },
    "CartoDB positron": {
        "tile": "CartoDB positron",
        "attribution": "Map tiles by CartoDB, under CC BY 3.0."
    },
    "CartoDB dark_matter": {
        "tile": "CartoDB dark_matter",
        "attribution": "Map tiles by CartoDB, under CC BY 3.0."
    },
}


for _, row in towereLocation.iterrows():
    if row['Network']== 'Vodacom':
      color = 'red'
    elif row['Network']== 'Econet':
      color = 'blue'
    elif row['Network']== 'MTN':
      color = 'green'
    else:
      color = 'black'

    # popup_text = f"Network: {row['Network']}<br>Radio: {row['radio']}"
    popup_text = f"<strong>Network:</strong> {row['Network']}<br><strong>Radio:</strong> {row['radio']}"

    

    folium.Circle(
        location=[row['LAT'], row['LON']],  # Circle center (latitude, longitude)
        radius = 4000 ,  # Circle radius in meters
        color='black',  # Border color
        fill=True,  # Fill the circle
        fill_color=color,  # Fill color
        fill_opacity=0.4,  # Fill opacity
        popup= popup_text   # Popup with the city name
    ).add_to(m)


# Tittle of the App
st.title("📶 Cell Tower Distribution in Lesotho")
# Description
st.markdown("""
This interactive map illustrates the distribution of cell towers across Lesotho. 
The red dots signify the locations of towers operated by Vodacom Lesotho, while the blue dots represent those managed by Econet Lesotho, the two leading telecommunications providers in the country.
""")

st.write('**Click on the dots to see information about each cell Tower**')


# Creating a dropdown to select the tile
tile_choice = st.selectbox("Choose a map tile:", list(tiles.keys()))

# Adding the selected tile to the map with attribution
folium.TileLayer(tiles[tile_choice]["tile"], 
                 attr=tiles[tile_choice]["attribution"]).add_to(m)
folium.LayerControl().add_to(m)

# Displaying the map
folium_static(m, width=1000, height=1000)

# Uses of the App
st.subheader("Uses of the App")
uses = [
    "**Tourism:**",
    "- Travelers can identify areas with reliable mobile coverage, enhancing connectivity and accessibility during their visits.",
    "- Tour operators can use the data to plan tours in regions with better network access, ensuring seamless communication for both guides and tourists.",
    
    "**Tech Startups:**",
    "- Entrepreneurs can analyze network coverage to determine optimal locations for launching tech-based services.",
    "- Startups focused on mobile applications can leverage this information to target areas with the highest potential user engagement.",
    
    "**Emergency Services:**",
    "- Authorities can utilize the map to assess communication capabilities in various regions, aiding in disaster response and emergency management.",
    
    "**Research and Development:**",
    "- Researchers can analyze the distribution patterns of cell towers to study the impact of telecommunications infrastructure on economic development and social connectivity."
]

for use in uses:
    st.markdown(use)

# Disclaimer
st.warning("Please note that the information presented may not be completely accurate, and users are encouraged to verify details as needed.")
