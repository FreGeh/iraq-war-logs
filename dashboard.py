import dash as dash
import dash.dependencies as dd
from flask_caching import Cache
from dash_extensions.enrich import DashProxy, MultiplexerTransform
from plots.plot1 import create_plot1_layout, create_plot1_callback
from plots.plot2 import create_plot2_layout
from plots.plot3 import create_plot3_layout, create_plot3_callback
from plots.plot4 import create_plot4_layout, create_plot4_callback
from plots.plot5 import create_plot5_layout, create_plot5_callback
import flask
server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

app.config.suppress_callback_exceptions = True

cache = Cache(server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': '/Users/ibm/Programming/datahirachy/cache'
})
cache.init_app(app.server)

app.layout = dash.html.Div([
    dash.dcc.Location(id='url', refresh=False),
    dash.html.Div([
        dash.html.Div([
            dash.html.H1('Data Visualization Assignment', style={'textAlign': 'center'}),
            dash.html.P('Aufgrund der großen Datenmenge kann das Laden etwas länger dauern (15-30 seconds).', style={'textAlign': 'center'}),
            dash.html.H3('Wähle einen der Plots aus:', style={'textAlign': 'center'}),
            dash.dcc.Tabs(id='tabs-example', value='plot1', children=[
                dash.dcc.Tab(label='Plot 1', value='plot1'),
                dash.dcc.Tab(label='Plot 2', value='plot2'),
                dash.dcc.Tab(label='Plot 3', value='plot3'),
                dash.dcc.Tab(label='Plot 4', value='plot4'),
                dash.dcc.Tab(label='Plot 5', value='plot5'),
            ]),
        ]),
    ]),
    dash.html.Div(id='tabs-content-example'),
])
@app.callback(dd.Output('tabs-content-example', 'children'),
              dd.Input('tabs-example', 'value'))
@cache.memoize(timeout=600)
def render_content(tab):
    if tab == 'plot1':
        return create_plot1_layout()
    elif tab == 'plot2':
        return create_plot2_layout()
    elif tab == 'plot3':
        return create_plot3_layout()
    elif tab == 'plot4':
        return create_plot4_layout()
    elif tab == 'plot5':
        return create_plot5_layout()


create_plot1_callback(app)
create_plot3_callback(app)
create_plot4_callback(app)
create_plot5_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)
