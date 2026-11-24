from dash import dcc 
from dash import html
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import pandas as pd

def create_plot4_layout():
    return html.Div([
        html.H1('Plot 4: Civilian Casualties by Reported Affiliation'),
        html.Button('Include Wounded', id='wia-button', className='cool-button'),
        dcc.Graph(id='plot4-graph'),  # Plot 4 layout: a graph component
        html.P(
            'Affiliation comes from the “Attack on” field in the original reports. '
            'The chart includes only reports with at least two civilian deaths.',
            className='my-p',
        ),
    ])


def create_plot4_callback(app):
    @app.callback(
        Output('plot4-graph', 'figure'),
        Output('wia-button', 'children'),
        [Input('wia-button', 'n_clicks')]
    )
    def update_plot(n_clicks):
        show_wounded = (n_clicks or 0) % 2 == 1
        df = pd.read_csv("./iraq1.csv")
        df = df[df['Affiliation'].isin(['FRIEND', 'ENEMY'])]
        df = df[df['Civilian_KIA'] > 1]  # Only include cases where Civilian_KIA is greater than 1

        traces = []

        color_dict = {'FRIEND': 'green', 'ENEMY': 'red'}  # Assign colors to each affiliation

        for affil in ['FRIEND', 'ENEMY']:
            traces.append(
                go.Violin(
                    y=df[df['Affiliation'] == affil]['Civilian_KIA'],
                    name=f"Fatalities · {affil}",
                    line_color=color_dict[affil],  # Use the designated color for this affiliation
                    box_visible=False,
                    meanline_visible=False,
                    hovertemplate = 
                    '<b>Affiliation</b>: %{x}<br>'+
                    '<b>Fatalities</b>: %{y}<extra></extra>'
                )
            )
            if show_wounded:
                traces.append(
                    go.Violin(
                        y=df[df['Affiliation'] == affil]['Civilian_WIA'],
                        name=f"Wounded · {affil}",
                        line_color=color_dict[affil],  # Use the designated color for this affiliation
                        box_visible=False,
                        meanline_visible=False,
                        hovertemplate = 
                        '<b>Affiliation</b>: %{x}<br>'+
                        '<b>Wounded</b>: %{y}<extra></extra>'
                    )
                )

        layout = go.Layout(
            title="Distribution of Civilian Fatalities and Wounded by Affiliation",
            yaxis=dict(
                title="Number of Civilian Fatalities and Wounded",
                type='log'  # Log scale to better visualize skewed distributions
            ),
            xaxis=dict(
                title="Reported affiliation"
            )
        )

        fig = go.Figure(data=traces, layout=layout)

        return fig, 'Hide Wounded' if show_wounded else 'Include Wounded'
