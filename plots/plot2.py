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

df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Month'] = df['Datetime'].dt.to_period('M')

df_grouped = df.groupby(['Region', 'Month'])[['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA']].sum().reset_index()
df_grouped['Total_KIA'] = df_grouped[['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA']].sum(axis=1)

# Calculate percentages
for col_name in ['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA']:
    df_grouped[col_name + '_Percentage'] = np.where(
        df_grouped['Total_KIA'] > 0,
        df_grouped[col_name] / df_grouped['Total_KIA'] * 100,
        0
    )

# Merge with the geojson data
for feature in data['features']:
    feature['id'] = feature['properties']['NAME_1']

df_grouped['Month'] = df_grouped['Month'].astype(str)


def create_plot2_layout():

    fig = go.Figure()

    # Define base traces (for the first available month)
    first_month = df_grouped.Month.min()
    first_df = df_grouped[df_grouped.Month == first_month]
    kia_types = ['Enemy_KIA_Percentage', 'Friend_KIA_Percentage', 
                 'Civilian_KIA_Percentage', 'Host_nation_KIA_Percentage']

    # Base traces: GeoJSON is included only once
    for i, kia_type in enumerate(kia_types):
        fig.add_trace(
            go.Choroplethmapbox(
                geojson=data,
                locations=first_df['Region'],
                z=first_df[kia_type],
                colorscale="YlOrRd",
                zmin=0,
                zmax=100,
                marker_opacity=0.9,
                marker_line_width=0,
                name=kia_type,
                visible=(kia_type == 'Civilian_KIA_Percentage')  # Same logic as before
            )
        )

    # Build animation frames
    frames = []
    unique_months = df_grouped.Month.unique()

    for month in unique_months:
        month_df = df_grouped[df_grouped.Month == month]
        frame_data = []
        for kia_type in kia_types:
            frame_data.append(
                go.Choroplethmapbox(
                    locations=month_df['Region'],
                    z=month_df[kia_type],
                    colorscale="YlOrRd",
                    zmin=0,
                    zmax=100,
                    marker_opacity=0.9,
                    marker_line_width=0
                )
            )
        frames.append(go.Frame(data=frame_data, name=month))

    fig.frames = frames

    # Update layout with animation controls and filters
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
                    dict(label="Civilian Deaths %", 
                         method="update", 
                         args=[{"visible": [False, False, True, False]}]),
                    dict(label="Enemy Forces Deaths %", 
                         method="update", 
                         args=[{"visible": [True, False, False, False]}]),
                    dict(label="Friendly Force Deaths %", 
                         method="update", 
                         args=[{"visible": [False, True, False, False]}]),
                    dict(label="Iraqi Forces Deaths %", 
                         method="update", 
                         args=[{"visible": [False, False, False, True]}]),
                ]),
            ),
        ],
        sliders=[
            dict(
                steps=[
                    dict(
                        method="animate",
                        args=[
                            [str(month)],  # Frame to animate to
                            {
                                "frame": {"duration": 300, "redraw": True},
                                "mode": "immediate",
                                "transition": {"duration": 300},
                            },
                        ],
                        label=str(month)  
                    )
                    for month in unique_months
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
        mapbox_zoom=4,
        mapbox_center={"lat": 33.3152, "lon": 44.3661},
        title="Fatalities by Responsibility Zone", 
    )

    layout = html.Div([
        html.H1('Plot 2: Geographic Distribution of Fatalities'),
        dcc.Graph(id='choropleth-plot', figure=fig),
        html.H4('Military Responsibility Zones:'),
        html.Ul([
            html.Li(html.B("MNF-W: Multinational Forces West")),
            html.Li(html.B("MND-N: Multinational Division North")),
            html.Li(html.B("MND-BAGHDAD: Multinational Division Baghdad")),
            html.Li(html.B("MND-C: Multinational Division Central Iraq")),
            html.Li(html.B("MND-SE: Multinational Division Southeast")),
        ])
    ])

    return layout
