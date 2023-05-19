import dash as dash
import dash.dependencies as dd
from plots.plot1 import create_plot1_layout, create_plot1_callback
from plots.plot2 import create_plot2_layout
from plots.plot3 import create_plot3_layout, create_plot3_callback
from plots.plot4 import create_plot4_layout, create_plot4_callback
from plots.plot5 import create_plot5_layout, create_plot5_callback
import flask

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server)

app.config.suppress_callback_exceptions = True


app.layout = dash.html.Div(className="container", children=[
    dash.dcc.Location(id='url', refresh=False),
    dash.html.Div(className='my-div', children=[
        dash.html.H1('Irakkrieg Visualisierung', className='my-h1'),
        dash.html.P('Aufgrund der großen Datenmenge kann das Laden etwas länger dauern (10-20 Sekunden).', className='my-p'),
        dash.html.H3('Wähle eine der Darstellungen aus:', className='my-h3'),
        dash.dcc.Tabs(id='tabs-example', value='plot1', className='my-tabs', children=[
            dash.dcc.Tab(label='Zeitstrahl', value='plot1', className='my-tab'),
            dash.dcc.Tab(label='Regionalität', value='plot2', className='my-tab'),
            dash.dcc.Tab(label='Ursachen', value='plot3', className='my-tab'),
            dash.dcc.Tab(label='Verursacher', value='plot4', className='my-tab'),
            dash.dcc.Tab(label='Tötlichkeit', value='plot5', className='my-tab'),
        ]),
    ]),
    dash.html.Div(id='tabs-content-example', className='my-content'),
])


@app.callback(dd.Output('tabs-content-example', 'children'),
              dd.Input('tabs-example', 'value'))
def render_content(tab):
    if tab == 'plot1':
        return dash.html.Div(
            className='my-content plot1',
            children=[create_plot1_layout()]
        )
    elif tab == 'plot2':
        return dash.html.Div(
            className='my-content plot2',
            children=[create_plot2_layout()]
        )
    elif tab == 'plot3':
        return dash.html.Div(
            className='my-content plot3',
            children=[create_plot3_layout()]
        )
    elif tab == 'plot4':
        return dash.html.Div(
            className='my-content plot4',
            children=[create_plot4_layout()]
        )
    elif tab == 'plot5':
        return dash.html.Div(
            className='my-content plot5',
            children=[create_plot5_layout()]
        )


create_plot1_callback(app)
create_plot3_callback(app)
create_plot4_callback(app)
create_plot5_callback(app)

if __name__ == '__main__':
    app.run_server(debug=True)
