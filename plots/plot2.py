import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np
from urllib.request import urlopen
from dash import dcc
from dash import html


with open("./merged_provinces.geojson") as f:
    data = json.load(f)

# Read the CSV
df = pd.read_csv('./iraq1.csv')

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
        fig.add_trace(go.Choroplethmapbox(visible=(kia_type == 'Civilian_KIA_Percentage'),  # changed here
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
        ], name=month))  # frame name is just the 'month'

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
            x=0,
            xanchor="left",
            y=1.2,
            yanchor="top",
            buttons=list([
                dict(label="Civilian Deaths %", method="update", args=[{"visible": [False, False, True, False]}]),  # changed here
                dict(label="Enemy Forces Deaths %", method="update", args=[{"visible": [True, False, False, False]}]),
                dict(label="Friendly Force Deaths %", method="update", args=[{"visible": [False, True, False, False]}]),
                dict(label="Iraqi Forces Deaths %", method="update", args=[{"visible": [False, False, False, True]}]),
            ]),
        ),
    ],
    sliders=[
        dict(
            steps=[
                dict(
                    method="animate",
                    args=[
                        [str(month)],  # frame to animate to
                        {
                            "frame": {"duration": 300, "redraw": True},
                            "mode": "immediate",
                            "transition": {"duration": 300},
                        },
                    ],
                    label=str(month)  # label is the 'month'
                )
                for month in df_grouped.Month.unique()
            ],
            active=0,
            transition={"duration": 300},
            x=0,
            y=0,
            currentvalue=dict(
                font=dict(size=12),
                prefix="Monat: ",
                visible=True,
                xanchor="center"
            )
        )
    ],
    mapbox_style="carto-positron",
    mapbox_zoom=4,
    mapbox_center={"lat": 33.3152, "lon": 44.3661},  # approximate center of Iraq
    title="Todesfälle nach Verantwortungsbereich", 
    )

    layout = html.Div([
        html.H1('Plot 2: Geografische Einteilung der Todesfälle'),
        dcc.Graph(id='choropleth-plot', figure=fig),  # wrap the figure in a dcc.Graph
        html.H4('Verantwortungsbereiche:'),
        html.P('MNF-W: Multinationale Streitkräfte im Westen; MND-N: Multinationale Division im Norden; MND-BAGHDAD: Multinationale Division in Bagdad; MND-C: Multinationale Division in Zentral-Irak; MND-SE: Multinationale Division im Südosten')
    ])

    return layout