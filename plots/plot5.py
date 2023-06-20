import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
import numpy as np

def create_plot5_layout():
    return html.Div([
        html.H1('Plot 5: Zivile Opfer unterteilt nach Typ der Ursache'),
        html.Button('Skala Wechseln (Linear/Log)', id='log-button', className='cool-button'),
        dcc.Graph(id='plot5-graph'),  # Plot layout: a graph component
    ])


def create_plot5_callback(app):
    @app.callback(
        Output('plot5-graph', 'figure'),
        Input('plot5-graph', 'id'),  # change the input to the id of the graph itself
        Input('log-button', 'n_clicks')
    )
    def update_plot(id, n_clicks):
        df = pd.read_csv("./iraq1.csv")
        df['Civilian_Casualties'] = df['Civilian_KIA'] + df['Civilian_WIA']

        # Exclude "NONE SELECTED" and "OTHER" types
        types = df[df['Type'].isin(['NONE SELECTED', 'OTHER']) == False]['Type'].unique()

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
            title="Durchschnittliche Zivile Tote und Verwundete pro Kategorie und Typ",
            xaxis=dict(
                title="Durchschnittliche Anzahl Tote und Verwundete",
                type=xaxis_type
            ),
            yaxis=dict(
                title="Typ",
                type='category'
            ),
            hovermode='closest'
        )

        fig = go.Figure(data=data, layout=layout)
        
        return fig
