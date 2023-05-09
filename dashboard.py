import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output
from plots.plot1 import create_plot1_layout, create_plot1_callback

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
            html.Div([
                html.H2('Dashboard'),
                html.P('Öffne den entsprechenden Plot:'),
                html.Div(className='tab', children=[
                    html.Button('Plot 1', id='plot1-button', className='tablinks'),
                    html.Button('Plot 2', id='plot2-button', className='tablinks'),
                    html.Button('Plot 3', id='plot3-button', className='tablinks')
                ]),
            ]),
        ]),
    html.Div(id='page-content'),
    ]),
])


@app.callback(Output('page-content', 'children'),
              [Input('plot1-button', 'n_clicks'),
               Input('plot2-button', 'n_clicks'),
               Input('plot3-button', 'n_clicks')])
def display_page(n_clicks_plot1, n_clicks_plot2, n_clicks_plot3):
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.Div([])
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'plot1-button':
        return create_plot1_layout()
    elif button_id == 'plot2-button':
        # Replace with your plot 2 layout
        return html.Div([html.H3('Plot 2')])
    elif button_id == 'plot3-button':
        # Replace with your plot 3 layout
        return html.Div([html.H3('Plot 3')])


create_plot1_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)
