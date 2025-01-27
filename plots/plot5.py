from dash import dcc 
from dash import html
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
import numpy as np

def create_plot5_layout():
    return html.Div([
        html.H1('Plot 5: Civilian Casualties by Cause Type'),
        html.Button('Toggle Scale (Linear/Log)', id='log-button', className='cool-button'),
        dcc.Graph(id='plot5-graph'),  # Plot layout: a graph component
    ])


def create_plot5_callback(app):
    @app.callback(
        Output('plot5-graph', 'figure'),
        Input('plot5-graph', 'id'),  # Change the input to the graph's ID
        Input('log-button', 'n_clicks')
    )
    def update_plot(id, n_clicks):
        df = pd.read_csv("./iraq1.csv")
        df['Civilian_Casualties'] = df['Civilian_KIA'] + df['Civilian_WIA']

        # Exclude "NONE SELECTED" and "OTHER" types
        types = df[~df['Type'].isin(['NONE SELECTED', 'OTHER'])]['Type'].unique()

        data = []

        for t in types:
            categories = df[df['Type'] == t]['Category'].unique()
            averages = []

            for cat in categories:
                average = df[(df['Category'] == cat) & (df['Type'] == t)]['Civilian_Casualties'].mean()
                averages.append(average)

            trace = go.Scatter(
                y=[t]*len(averages),
                x=averages,
                mode='markers',
                name=t,
                marker=dict(
                    size=10,
                    line=dict(
                        width=2,
                        color='rgba(0, 0, 0, .8)'
                    )
                ),
                text=categories,
                hovertemplate='%{text}<br>Avg: %{x}'
            )

            data.append(trace)

        # Determine whether the x-axis should be linear or logarithmic
        xaxis_type = 'log' if n_clicks and n_clicks % 2 != 0 else 'linear'

        layout = go.Layout(
            title="Average Civilian Fatalities and Wounded per Category and Cause Type",
            xaxis=dict(
                title="Average Number of Fatalities and Wounded",
                type=xaxis_type
            ),
            yaxis=dict(
                title="Cause Type",
                type='category'
            ),
            hovermode='closest'
        )

        fig = go.Figure(data=data, layout=layout)
        
        return fig
