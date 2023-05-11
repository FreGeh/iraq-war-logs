import json
import geopandas as gpd
import plotly.express as px
import pandas as pd

# Load GeoJSON file
with open("datahirachy/merged_provinces.geojson") as f:
    data = json.load(f)

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(data["features"])

# Read the CSV
df = pd.read_csv('datahirachy/iraq.csv')

# Convert 'Datetime' column to datetime and extract the month
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Month'] = df['Datetime'].dt.to_period('M')

# Group by Region and Month and sum the KIA columns
df_grouped = df.groupby(['Region', 'Month'])[['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA']].sum().reset_index()

# Merge with the geo dataframe
merged = gdf.merge(df_grouped, left_on='NAME_1', right_on='Region', how='inner')


# Define a function to create a map for a particular month
def create_map_for_month(year_month):
    filtered = merged[merged['Month'] == year_month]
    fig = px.choropleth_mapbox(filtered, geojson=filtered.geometry, 
                               color='Enemy_KIA',  # replace with the column you want to visualize
                               mapbox_style="carto-positron",
                               color_continuous_scale="Viridis",
                               labels={'NAME_1':'Coalition Force'},  # update labels as per your data
                               zoom=5, center = {"lat": filtered.geometry.centroid.y.mean(), "lon": filtered.geometry.centroid.x.mean()},
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.show()

# Create a map for January 2004
create_map_for_month(pd.Period('2004-01'))
