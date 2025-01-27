import pandas as pd 
import plotly.graph_objs as go
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Load dataset
df = pd.read_csv("./iraq1.csv")

# Convert relevant columns to numeric type
numeric_cols = ['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA',
                'Enemy_WIA', 'Friend_WIA', 'Civilian_WIA', 'Host_nation_WIA']
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

# Grouped dataframes
df_grouped_counts = df.groupby(['Type', 'Category']).size().reset_index(name='Counts')
df_grouped_sum = df.groupby(['Type', 'Category'])[numeric_cols].sum().reset_index()

# Dropdown options
options = [
    {'label': 'Total Incidents', 'value': 'Counts'},
    {'label': 'Civilian Killed', 'value': 'Civilian_KIA'},
    {'label': 'Civilian Wounded', 'value': 'Civilian_WIA'},
    {'label': 'Enemy Forces Killed', 'value': 'Enemy_KIA'},
    {'label': 'Enemy Forces Wounded', 'value': 'Enemy_WIA'},
    {'label': 'Friendly Forces Killed', 'value': 'Friend_KIA'},
    {'label': 'Friendly Forces Wounded', 'value': 'Friend_WIA'},
    {'label': 'Iraqi Forces Killed', 'value': 'Host_nation_KIA'},
    {'label': 'Iraqi Forces Wounded', 'value': 'Host_nation_WIA'}
]   

def create_plot3_layout():
    layout = html.Div([
        html.H1('Plot 3: Categorical Distribution of Fatalities and Injuries by Cause'),
        dcc.Dropdown(
            id='dropdown',
            options=options,
            value=['Counts'],  # Default value
            multi=True,
            placeholder='Select a category'        
        ),
        dcc.Graph(id='treemap'),
        html.P('IED: Improvised Explosive Device')
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
            df_grouped_sum['sum_values'] = df_grouped_sum[values].sum(axis=1)  # Add new column for sum of selected values
            df_grouped = df_grouped_sum[df_grouped_sum['sum_values'] > 0]  # Remove zero-value entries
            value_column = 'sum_values'  # Set value_column for treemap
        else:
            value_column = 'Counts'  # Default to total incidents if no other values are selected

        fig = px.treemap(df_grouped, path=['Type', 'Category'], values=value_column,
                        color=value_column,
                        color_continuous_scale='YlOrRd',
                        title='Distribution of Incident Types by Category')
        return fig
