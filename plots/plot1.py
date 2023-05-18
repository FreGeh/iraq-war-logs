import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import datetime
from dash import no_update

# Sample data
df = pd.read_csv("./iraq.csv")

# Convert 'Datetime' column to datetime and extract the day
df['Datetime'] = pd.to_datetime(df['Datetime']).dt.date 

# Group by day and sum the KIA columns
df_grouped = df.groupby('Datetime')[['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA', 'Host_nation_KIA']].sum().reset_index()

colors = {
    'Enemy_KIA': 'red',
    'Friend_KIA': 'green',
    'Civilian_KIA': 'blue',
    'Host_nation_KIA': 'orange'
}

def create_plot1_layout():
    layout = html.Div([
        html.H1('Plot 1'),
        html.H3('Killed in Action:'),
        dcc.Checklist(
            id='attribute-selector',
            options=[
                {'label': 'Enemy Forces', 'value': 'Enemy_KIA'},
                {'label': 'Friendly Forces', 'value': 'Friend_KIA'},
                {'label': 'Iraqi Forces', 'value': 'Host_nation_KIA'},
                {'label': 'Civilians', 'value': 'Civilian_KIA'}
            ],
            value=['Civilian_KIA']
        ),
        dcc.Graph(id='bar-plot'),
    ])
    return layout

def create_plot1_callback(app):
    @app.callback(
            Output('bar-plot', 'figure'),
            [Input('attribute-selector', 'value')]
        )
    def update_combined_plot(selected_attributes):
        data = []

        for attribute in selected_attributes:
            data.append(go.Bar(x=df_grouped['Datetime'], y=df_grouped[attribute], name=attribute, marker_color=colors[attribute],
                                hovertemplate="<b>Deaths</b>: %{y} <br> <b>Day</b>: %{x}"))

            # Calculate 14-day moving average
            moving_average = df_grouped[attribute].rolling(window=14).mean()

            data.append(go.Scatter(x=df_grouped['Datetime'], y=moving_average, mode='lines', name=f"{attribute} 14-day MA", marker_color=colors[attribute],
                                    hovertemplate="<b>14-day Moving Avg</b>: %{y:.2f} <br> <b>Day</b>: %{x}"))

        fig = go.Figure(data=data)
        fig.update_layout(showlegend=True, title="Killed in Action per Day with 14-day Moving Averages", xaxis_title="Date", yaxis_title="Number of Deaths", barmode='stack')

        # Add range selector and range slider
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")                
                ])
            ),
            type="date"
        )

        return fig
