import dash
import dash_bootstrap_components as dbc
import dash
from dash import html
import plotly.graph_objects as go
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import sql_util
from app import app


def serve_cost():
    main_div = html.Div( id="cost_summary")
    results = sql_util.execute_sql("""
            select distinct keyword from click_by_day 
        """);

    options = dict()
    for keyword, in results:
        options[keyword] = keyword

    cost_dropdown = dcc.Dropdown(
            id="cost_dropdown",
            options=options,
            value=list(options.keys())[0]
        )
    cost_bar_plot = dcc.Graph(id="cost_bar_plot")

    main_div.children = [cost_dropdown, cost_bar_plot]

    return main_div 

@app.callback(
    Output(component_id="cost_bar_plot", component_property="figure"),
    [Input(component_id="cost_dropdown", component_property="value")],
)
def graph_update(dropdown_value):
    results = sql_util.execute_sql("""
            select day,total_cost, avg_cost from click_by_day where keyword=?
        """, bound_data=[(dropdown_value)]);

    days = []
    total_per_day = []
    average_per_day = []
    for day,total,average in results:
        days.append(day)
        total_per_day.append(total)
        average_per_day.append(average)
    fig = go.Figure(
        [
            go.Scatter(
                x=days,
                y=average_per_day,
                line=dict(color="firebrick", width=4),
            )
        ]
    )
    fig.update_layout(xaxis_title='Days', yaxis_title='Average Cost Per Click')
    return fig 
