import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from twitchanal.process.game import Game

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

game = Game()
df = game.get_data()
tags = game.get_tags()
labels = game.get_labels()


def draw_num_of_game_per_tag():
    data = {'tag': [], 'num': []}
    for key in labels.keys():
        data['tag'].append(key)
        data['num'].append(len(labels[key]))
    fig = px.pie(data,
                 names='tag',
                 values='num',
                 title='Number of Games per Tag')
    return fig


def draw_total_viewers():
    data = {'tag': [], 'total': []}
    for key in labels.keys():
        data['tag'].append(key)
        sdf = df[df['id'].isin(labels[key])]
        total = sdf['Avg. viewers, 7 days'].sum()
        data['total'].append(total)
    fig = px.bar(data, x='tag', y='total', title='Total Viewers in 7 Days')
    return fig


def draw_average_viewers():
    data = {'tag': [], 'aver': []}
    for key in labels.keys():
        data['tag'].append(key)
        sdf = df[df['id'].isin(labels[key])]
        aver = sdf['Avg. viewers, 7 days'].sum() *1.0 / len(labels[key])
        data['aver'].append(aver)
    fig = px.bar(data, x='tag', y='aver', title='Average Viewers in 7 Days')
    return fig



def draw_peak_viewers():
    data = {'tag': [], 'peak': []}
    for key in labels.keys():
        data['tag'].append(key)
        sdf = df[df['id'].isin(labels[key])]
        peak = sdf['Peak viewers '].str.split(' ').str[0].astype(int)
        data['peak'].append(peak.max())
    fig = px.bar(data, x='tag', y='peak', title='Peak Viewers')
    return fig


def draw_viewer_channel():
    data = {'channel': [], 'viewer': []}
    for _, row in df.iterrows():
        data['channel'].append(row['Avg. viewers, 7 days'])
        data['viewer'].append(row['Avg. channels, 7 days'])

    model = LinearRegression()
    model.fit(np.array(data['channel']).reshape(-1, 1), np.array(data['viewer']))
    trace1 = go.Scatter(
        x=data['channel'],
        y=data['viewer'],
        name='Viewer VS. Channel',
        mode = 'markers'
    )
    x_range = np.linspace(min(data['channel']), max(data['channel']), 100)
    y_range = model.predict(x_range.reshape(-1, 1))
    trace2 = go.Scatter(
        x=x_range,
        y=y_range,
        name='Line',
    )
    fig=go.Figure(data=[trace1, trace2])
    fig.update_layout(
        title='Viewers VS. Channels',
        xaxis_title='Channels Number',
        yaxis_title='Viewers',
    )
    return fig


## HTML layout for the web page
app.layout = html.Div(children=[
    html.H1(children='Twitch Analysis', style={'textAlign': 'center'}),

    # draw 2 plots in one row
    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Graph(id='num_of_game_per_tag_graph', figure=draw_num_of_game_per_tag()),
            ])
        ),
        dbc.Col(
            html.Div([
                dcc.Graph(id='total_viewers_graph', figure=draw_total_viewers()),
            ])
        )
    ]),

    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Graph(id='aver_viewers_graph', figure=draw_average_viewers()),
            ])
        ),
        dbc.Col(
            html.Div([
                dcc.Graph(id='peak_viewers_graph', figure=draw_peak_viewers()),
            ])
        ),
    ]),

    dcc.Graph(id='viewer_channel_graph', figure=draw_viewer_channel())
])


def show(debug: bool):
    app.run_server(debug=debug)
