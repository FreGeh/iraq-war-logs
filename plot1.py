import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import datetime

# Sample data
df = pd.read_csv("iraq_sigacts.csv")

# Convert 'Datetime' column to datetime and extract the day
df['Datetime'] = pd.to_datetime(df['Datetime']).dt.date

# Group by day and sum the KIA columns
df_grouped = df.groupby('Datetime')[['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA']].sum().reset_index()

# Set up Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Checklist(
        id='attribute-selector',
        options=[
            {'label': 'Enemy_KIA', 'value': 'Enemy_KIA'},
            {'label': 'Friend_KIA', 'value': 'Friend_KIA'},
            {'label': 'Civilian_KIA', 'value': 'Civilian_KIA'}
        ],
        value=['Civilian_KIA']
    ),
    dcc.Graph(id='bar-plot'),
    dcc.RangeSlider(
        id='date-slider',
        min=datetime.datetime.combine(df_grouped['Datetime'].min(), datetime.time.min).timestamp(),
        max=datetime.datetime.combine(df_grouped['Datetime'].max(), datetime.time.min).timestamp(),
        value=[
            datetime.datetime.combine(df_grouped['Datetime'].min(), datetime.time.min).timestamp(),
            datetime.datetime.combine(df_grouped['Datetime'].max(), datetime.time.min).timestamp()
        ],
        step=None,
),

])

# Colors for each attribute
colors = {
    'Enemy_KIA': 'red',
    'Friend_KIA': 'green',
    'Civilian_KIA': 'blue'
}

# ... (previous code remains the same)

# Callback function
@app.callback(
    Output('bar-plot', 'figure'),
    [Input('attribute-selector', 'value'), Input('date-slider', 'value')]
)
def update_combined_plot(selected_attributes, date_range):
    date_range = [pd.to_datetime(ts, unit='s').date() for ts in date_range]
    df_filtered = df_grouped[(df_grouped['Datetime'] >= date_range[0]) & (df_grouped['Datetime'] <= date_range[1])]

    data = []

    for attribute in selected_attributes:
        data.append(go.Bar(x=df_filtered['Datetime'], y=df_filtered[attribute], name=attribute, marker_color=colors[attribute],
                           hovertemplate="<b>Deaths</b>: %{y} <br> <b>Day</b>: %{x}"))

        # Calculate 14-day moving average
        moving_average = df_filtered[attribute].rolling(window=14).mean()

        data.append(go.Scatter(x=df_filtered['Datetime'], y=moving_average, mode='lines', name=f"{attribute} 14-day MA", marker_color=colors[attribute],
                               hovertemplate="<b>14-day Moving Avg</b>: %{y:.2f} <br> <b>Day</b>: %{x}"))

    fig = go.Figure(data=data)
    fig.update_layout(showlegend=True, title="Killed in Action per Day with 14-day Moving Averages", xaxis_title="Date", yaxis_title="Number of Deaths", barmode='stack')

    # Add range slider
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
