import dash
import dash_bootstrap_components as dbc
from dash import html
import plotly.graph_objects as go
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import sql_util


def serve_pixel():
    results = sql_util.execute_sql("""
        select 
            count(*), 
            strftime('%Y-%m-%d', request_time) 
        FROM pixel_event 
            group by 2
        """);

    xs = []
    ys = []
    for pixel_count,day in results:
        xs.append(day)
        ys.append(pixel_count)
    fig = go.Figure(
        [
            go.Scatter(
                x=xs,
                y=ys,
                line=dict(color="firebrick", width=4),
            )
        ]
    )
    fig.update_layout(xaxis_title='Days', yaxis_title='Pixel Counts')
    return html.Div(children=[dcc.Graph(id="pixel_bar_plot",figure=fig)])

