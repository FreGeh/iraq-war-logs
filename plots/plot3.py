# plot3.py
import pandas as pd
import plotly.graph_objs as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

df = pd.read_csv("./iraq1.csv")

# Convert relevant columns to numeric type
numeric_cols = ['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA',
                'Enemy_WIA', 'Friend_WIA', 'Civilian_WIA', 'Host_nation_WIA']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Grouped dataframes
df_grouped_counts = df.groupby(['Type', 'Category']).size().reset_index(name='Counts')
df_grouped_sum = df.groupby(['Type', 'Category'])[numeric_cols].sum().reset_index()

# Create a list of dictionaries for the dropdown
options = [
    {'label': 'Insgesamt', 'value': 'Counts'},
    {'label': 'Enemy_KIA', 'value': 'Enemy_KIA'},
    {'label': 'Friend_KIA', 'value': 'Friend_KIA'},
    {'label': 'Civilian_KIA', 'value': 'Civilian_KIA'},
    {'label': 'Host_nation_KIA', 'value': 'Host_nation_KIA'},
    {'label': 'Enemy_WIA', 'value': 'Enemy_WIA'},
    {'label': 'Friend_WIA', 'value': 'Friend_WIA'},
    {'label': 'Civilian_WIA', 'value': 'Civilian_WIA'},
    {'label': 'Host_nation_WIA', 'value': 'Host_nation_WIA'}
]   

def create_plot3_layout():
    layout = html.Div([
        dcc.Dropdown(
            id='dropdown',
            options=options,
            value='Counts'
        ),
        dcc.Graph(id='treemap')
    ])
    return layout

def create_plot3_callback(app):
    @app.callback(
        Output('treemap', 'figure'),
        [Input('dropdown', 'value')]
    )
    def update_treemap(value):
        if value == 'Counts':
            df_grouped = df_grouped_counts
        else:
            df_grouped = df_grouped_sum
            df_grouped = df_grouped[df_grouped[value] > 0]  # filter out zero values

        fig = px.treemap(df_grouped, path=['Type', 'Category'], values=value,
                        color=value,
                        color_continuous_scale='YlOrRd',
                        title='Verteilung der Typen auf Kateogrien')
        return fig
