import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

# Sample data
df = pd.read_csv("iraq_sigacts.csv")

# Convert 'Datetime' column to datetime and extract the year
df['Datetime'] = pd.to_datetime(df['Datetime'])
df['Year'] = df['Datetime'].dt.year

# Group by year and sum the KIA columns
df_grouped = df.groupby('Year')[['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA']].sum().reset_index()

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
    html.Button('Change Display', id='change', n_clicks=0),
])

# Farben für jedes Attribut
colors = {
    'Enemy_KIA': 'red',
    'Friend_KIA': 'green',
    'Civilian_KIA': 'blue'
}

# Callback function
@app.callback(
    Output('bar-plot', 'figure'),
    [Input('attribute-selector', 'value'), 
    Input('change', 'n_clicks')]
)
def update_bar_plot(selected_attributes, n_clicks):
    data = []

    #prozent für den button
    isPercentage = False
    if n_clicks is not None and n_clicks % 2 == 1:
        isPercentage = True

    for attribute in selected_attributes:
        y_values = df_grouped[attribute] #y werte gespeichert
        #unterscheidung prozent und normalen werten
        if isPercentage == True:
            y_values = y_values / df_grouped[['Enemy_KIA', 'Friend_KIA', 'Civilian_KIA']].sum(axis=1) * 100
            hovertemplate = "<b>Deaths</b>: %{y:.2f}% <br> <b>Year</b>: %{x}"
        else:
            hovertemplate = "<b>Deaths</b>: %{y} <br> <b>Year</b>: %{x}"
        data.append(go.Bar(x=df_grouped['Year'], y=y_values, name=attribute, marker_color = colors[attribute], hovertemplate=hovertemplate))
    
    title = "Killed in Action per Year"
    
    if isPercentage:
        title = "Killed in Action per Year %"
    fig = go.Figure(data=data)
    fig.update_layout(showlegend=True, barmode='stack', title=title, yaxis=dict(range=[0, 100 if isPercentage else df_grouped[['Enemy_KIA']].values.max() + df_grouped[['Friend_KIA']].values.max() + df_grouped[['Civilian_KIA']].values.max()]))
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
