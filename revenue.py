import dash
import dash_bootstrap_components as dbc
import dash
from dash import html
import plotly.graph_objects as go
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from app import (
    app,
)  # ugly, but necessary, see: https://stackoverflow.com/questions/62102453/how-to-define-callbacks-in-separate-files-plotly-dash
import sql_util


def serve_revenue():
    main_div = html.Div( id="revenue_summary",)
    results = sql_util.execute_sql("""
            select distinct product_name, product_id from product_line_item_sale 
        """);

    options = dict()
    for product_name,product_id in results:
        options[product_id] = product_name

    revenue_dropdown = dcc.Dropdown(
            id="revenue_dropdown",
            options=options,
            value=list(options.keys())[0]
        )
    revenue_bar_plot = dcc.Graph(id="revenue_bar_plot")

    main_div.children = [revenue_dropdown, revenue_bar_plot]

    return main_div 

@app.callback(
    Output(component_id="revenue_bar_plot", component_property="figure"),
    [Input(component_id="revenue_dropdown", component_property="value")],
)
def graph_update(dropdown_value):
    print(dropdown_value)
    results = sql_util.execute_sql("""
            select day, total_revenue, avg_revenue from product_by_day where product_id=?
        """, bound_data=[(dropdown_value)]);

    days = []
    print(days)
    total_per_day = []
    average_per_day = []
    for day,total,average_revenue in results:
        days.append(day)
        total_per_day.append(total)
        average_per_day.append(average_revenue)
    print(days)
    fig = go.Figure(
        [
            go.Scatter(
                x=days,
                y=average_per_day,
                line=dict(color="firebrick", width=4),
            )
        ]
    )
    fig.update_layout(xaxis_title='Days', yaxis_title='Average Revenue $')
    print(fig)
    return fig 
