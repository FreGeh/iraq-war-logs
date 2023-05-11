import json
import geopandas as gpd
import plotly.express as px
import pandas as pd

# Load GeoJSON file
with open("datahirachy/merged_provinces.geojson") as f:
    data = json.load(f)

df = pd.read_csv('iraq.csv')

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(data["features"])

# Assuming 'NAME_1' field is the province name in your geojson
fig = px.choropleth_mapbox(gdf, geojson=gdf.geometry, locations=gdf.index,
                           color='NAME_1',  # or any other field you want to color by
                           mapbox_style="carto-positron",
                           color_continuous_scale="Viridis",
                           labels={'NAME_1':'Coalition Force'},  # update labels as per your data
                           zoom=5, center = {"lat": gdf.geometry.centroid.y.mean(), "lon": gdf.geometry.centroid.x.mean()},
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
