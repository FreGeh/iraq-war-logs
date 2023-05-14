import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np
from urllib.request import urlopen
import dash_core_components as dcc
import dash_html_components as html


with open("merged_provinces.geojson") as f:
    data = json.load(f)

# Read the CSV
df = pd.read_csv('iraq.csv')

# Convert 'Datetime' column to datetime and extract the month
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Month'] = df['Datetime'].dt.to_period('M')

# Group by Region and Month and sum the KIA columns
df_grouped = df.groupby(['Region', 'Month'])[['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA']].sum().reset_index()

# Calculate the sum of the four columns
df_grouped['Total_KIA'] = df_grouped[['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA']].sum(axis=1)

months = np.sort(df_grouped.Month.unique())

# Function to calculate percentages
def calculate_percentage(col_name):
    df_grouped[col_name + '_Percentage'] = np.where(df_grouped['Total_KIA'] > 0, 
                                                    df_grouped[col_name] / df_grouped['Total_KIA'] * 100, 
                                                    0)

# Apply function to each KIA type
for kia_type in ['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA']:
    calculate_percentage(kia_type)

# Merge with the geojson data
for feature in data['features']:
    feature['id'] = feature['properties']['NAME_1']

# Convert 'Month' to string for animation_frame
df_grouped['Month'] = df_grouped['Month'].astype(str)

def create_plot2_layout():

    fig = go.Figure()

    # Create a trace for each kia_type in the first month
    for kia_type in ['Enemy_KIA_Percentage', 'Friend_KIA_Percentage', 'Civilian_KIA_Percentage', 'Host_nation_KIA_Percentage']:
        fig.add_trace(go.Choroplethmapbox(visible=(kia_type == 'Enemy_KIA_Percentage'),
                                        geojson=data, 
                                        locations=df_grouped.loc[df_grouped.Month == df_grouped.Month.min(), 'Region'], 
                                        z=df_grouped.loc[df_grouped.Month == df_grouped.Month.min(), kia_type], 
                                        colorscale="YlOrRd",
                                        zmin=0,
                                        zmax=100,
                                        marker_opacity=0.9, 
                                        marker_line_width=0,
                                        name=kia_type))

    frames = []  # Create a list to store frames

    # Create a frame for each month
    for month in df_grouped.Month.unique():
        month_df = df_grouped[df_grouped.Month == month]
        frames.append(go.Frame(data=[
            go.Choroplethmapbox(geojson=data, 
                                locations=month_df.Region, 
                                z=month_df[kia_type], 
                                colorscale="YlOrRd",
                                zmin=0,
                                zmax=100,
                                marker_opacity=0.9, 
                                marker_line_width=0)
            for kia_type in ['Enemy_KIA_Percentage', 'Friend_KIA_Percentage', 'Civilian_KIA_Percentage', 'Host_nation_KIA_Percentage']
        ], name=f'{month}'))

    fig.frames = frames  # Assign the list of frames to fig.frames

    fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            buttons=list([
                dict(
                    label="Play",
                    method="animate",
                    args=[
                        None,
                        {
                            "frame": {"duration": 500, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 300, "easing": "quadratic-in-out"},
                        },
                    ],
                ),
                dict(
                    label="Pause",
                    method="animate",
                    args=[
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                ),
            ]),
        ),
        dict(
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top",
            buttons=list([
                dict(label="Enemy_KIA_Percentage", method="update", args=[{"visible": [True, False, False, False]}]),
                dict(label="Friend_KIA_Percentage", method="update", args=[{"visible": [False, True, False, False]}]),
                dict(label="Civilian_KIA_Percentage", method="update", args=[{"visible": [False, False, True, False]}]),
                dict(label="Host_nation_KIA_Percentage", method="update", args=[{"visible": [False, False, False, True]}]),
            ]),
        ),
    ],
    sliders=[
    dict(
        steps=[
            dict(
                method="animate",
                args=[
                    [f"{kia_type}_{str(month)}"],  # Convert the Period object to a string
                    {
                        "frame": {"duration": 300, "redraw": True},
                        "fromcurrent": True,
                        "transition": {"duration": 300},
                    },
                ],
                label=str(month)  # Convert the Period object to a string
            )
            for kia_type in ['Enemy_KIA_Percentage', 'Friend_KIA_Percentage', 'Civilian_KIA_Percentage', 'Host_nation_KIA_Percentage']
            for month in months
        ],
        active=0,
        transition={"duration": 300},
        x=0,
        y=0,
        currentvalue=dict(
            font=dict(size=12),
            prefix="Month: ",
            visible=True,
            xanchor="center"
        )
    )
    
],




    mapbox_style="carto-positron",
    mapbox_zoom=3,
    mapbox_center={"lat": 33.3152, "lon": 44.3661},  # approximate center of Iraq
    title="Killed in Action by Region",
)




    layout = html.Div([
        html.H1('Plot 2'),
        dcc.Graph(id='choropleth-plot', figure=fig),  # wrap the figure in a dcc.Graph
    ])

    return layout