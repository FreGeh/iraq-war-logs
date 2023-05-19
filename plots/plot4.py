import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd

def create_plot4_layout():
    return html.Div([
        html.H1('Plot 4: Zivile Opfer unterteilt nach Zugehörigkeit der Verursacher'),
        html.Button('Auch Verwundete miteinbeziehen', id='wia-button', className='cool-button'),
        dcc.Graph(id='plot4-graph'),  # Plot 4 layout: a graph component
    ])


def create_plot4_callback(app):
    @app.callback(
        Output('plot4-graph', 'figure'),
        [Input('wia-button', 'n_clicks')]
    )
    def update_plot(n_clicks):
        df = pd.read_csv("./iraq1.csv")
        df = df[df['Affiliation'].isin(['FRIEND', 'ENEMY'])]
        df = df[df['Civilian_KIA'] > 1]  # Only consider Civilian_KIA greater than 1

        traces = []

        color_dict = {'FRIEND': 'green', 'ENEMY': 'red'}  # Map each affiliation to a color

        for affil in ['FRIEND', 'ENEMY']:
            traces.append(
                go.Violin(
                    y=df[df['Affiliation'] == affil]['Civilian_KIA'],
                    name=affil + " (Tote)",
                    line_color=color_dict[affil],  # Use the corresponding color for this affiliation
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
                        name= affil + " (Verwundete)",
                        line_color=color_dict[affil],  # Use the corresponding color for this affiliation
                        box_visible=True,
                        meanline_visible=True,
                        hovertemplate = 
                        '<b>Zugehörigkeit</b>: %{x}<br>'+
                        '<b>Verwundete</b>: %{y}<extra></extra>'
                    )
                )

        layout = go.Layout(
            title="Verteilung der Toten und Verwundeten für jede Zugehörigkeit",
            yaxis=dict(
                title="Anzahl der Zivilen Toten und Verwundeten",
                type='log'  # Using a log scale can help with skewed distributions
            ),
            xaxis=dict(
                title="Verursacht durch"
            )
        )

        fig = go.Figure(data=traces, layout=layout)

        return fig
