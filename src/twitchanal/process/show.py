import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Twitch Analysis'),

    # dcc.Graph(
    #     id='example-graph',
    #     figure=fig
    # )
])

def show(debug: bool):
    app.run_server(debug=debug)
