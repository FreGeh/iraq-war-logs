import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd

def create_plot4_layout():
    return html.Div([
        dcc.Graph(id='plot4-graph'),  # Plot 4 layout: a graph component
        html.Button('Include Civilian_WIA', id='wia-button')
    ])


def create_plot4_callback(app):
    @app.callback(
        Output('plot4-graph', 'figure'),
        [Input('wia-button', 'n_clicks')]
    )
    def update_plot(n_clicks):
            df = pd.read_csv("./iraq.csv")
            df = df[df['Affiliation'].isin(['FRIEND', 'ENEMY'])]
            df = df[df['Civilian_KIA'] > 1]  # Only consider Civilian_KIA greater than 1

            traces = []

            for affil in ['FRIEND', 'ENEMY']:
                traces.append(
                    go.Violin(
                        y=df[df['Affiliation'] == affil]['Civilian_KIA'],
                        name=affil + ' KIA',
                        box_visible=True,
                        meanline_visible=True,
                        hovertemplate = 
                        '<b>Zugehörigkeit</b>: %{x}<br>'+
                        '<b>Todesfälle</b>: %{y}<extra></extra>'
                    )
                )
                if n_clicks is not None and n_clicks > 0:
                    traces.append(
                        go.Violin(
                            y=df[df['Affiliation'] == affil]['Civilian_WIA'],
                            name=affil + ' WIA',
                            box_visible=True,
                            meanline_visible=True,
                            hovertemplate = 
                            '<b>Zugehörigkeit</b>: %{x}<br>'+
                            '<b>Verletzte</b>: %{y}<extra></extra>'
                        )
                    )

            layout = go.Layout(
                title="Verteilung der Todesfälle und Verletzungen für jede Zugehörigkeit",
                yaxis=dict(
                    title="Anzahl der Zivilen Tote und Verletzte",
                    type='log'  # Using a log scale can help with skewed distributions
                ),
                xaxis=dict(
                    title="Verursacht durch"
                )
            )

            fig = go.Figure(data=traces, layout=layout)

            return fig
