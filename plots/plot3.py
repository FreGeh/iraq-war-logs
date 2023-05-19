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
    {'label': 'Civilian Killed', 'value': 'Civilian_KIA'},
    {'label': 'Civilian Wounded', 'value': 'Civilian_WIA'},
    {'label': 'Enemy Force Killed', 'value': 'Enemy_KIA'},
    {'label': 'Enemy Force Wounded', 'value': 'Enemy_WIA'},
    {'label': 'Friendly Force Killed', 'value': 'Friend_KIA'},
    {'label': 'Friendly Force Wounded', 'value': 'Friend_WIA'},
    {'label': 'Iraqi Force Killed', 'value': 'Host_nation_KIA'},
    {'label': 'Iraqi Force Wounded', 'value': 'Host_nation_WIA'}
]   

def create_plot3_layout():
    layout = html.Div([
        html.H1('Plot 3: Kategorische Einteilung der Toten und Verwundete nach Verusachungsgrund'),
        dcc.Dropdown(
            id='dropdown',
            options=options,
            value=['Counts'],  # default value as a list
            multi=True,
            placeholder='Wähle eine Kategorie aus'        
        ),
        dcc.Graph(id='treemap')
    ])
    return layout

from dash.dependencies import Input, Output, State

def create_plot3_callback(app):
    @app.callback(
        Output('dropdown', 'value'),
        [Input('dropdown', 'value')],
        [State('dropdown', 'value')]
    )
    def update_dropdown_value(new_values, old_values):
        if 'Counts' in new_values and len(new_values) > 1:
            return [value for value in new_values if value != 'Counts']
        else:
            return new_values

    @app.callback(
        Output('treemap', 'figure'),
        [Input('dropdown', 'value')]
    )
    def update_treemap(values):
        df_grouped = pd.DataFrame()

        if 'Counts' in values:
            df_grouped = df_grouped_counts
            values.remove('Counts')

        # If other values selected, sum them
        if values: 
            df_grouped_sum['sum_values'] = df_grouped_sum[values].sum(axis=1)  # add new column for sum of values
            df_grouped = df_grouped_sum[df_grouped_sum['sum_values'] > 0]  # filter out zero values
            value_column = 'sum_values'  # set value_column to the new column for treemap
        else:
            value_column = 'Counts'  # if no other values, set value_column to Counts

        fig = px.treemap(df_grouped, path=['Type', 'Category'], values=value_column,
                        color=value_column,
                        color_continuous_scale='YlOrRd',
                        title='Verteilung der Typen auf Kateogrien')
        return fig
