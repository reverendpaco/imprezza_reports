from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sql_util


df = px.data.stocks()


def serve_summary():
    main_div = html.Div( id="parent",)
    order_count,latest_time_orders,earliest_time_orders = sql_util.execute_sql_one("""
        select 
            count(*), 
            max(strftime('%Y-%m', creation_time)), 
            min(strftime('%Y-%m', creation_time)) 
        FROM order_transaction""");
    line_item_count,avg_revenue = sql_util.execute_sql_one("""
        select 
            sum(unit_count), 
            avg(unit_count * actual_price_per )   
        FROM product_line_item_sale""");
    line_item_count,avg_revenue = sql_util.execute_sql_one("""
        select 
            sum(unit_count), 
            avg(unit_count * actual_price_per )   
        FROM product_line_item_sale""");
    period = dcc.Markdown(
        id='total-orders',
        children=f'Perdod from  {latest_time_orders} to  {earliest_time_orders}.'
    )
    total_orders_by_period = dcc.Markdown(
        id='total-orders',
        children=f'There are **{order_count}** total orders in this period.'
    )
    total_line_items = dcc.Markdown(
        id='total-product-sales',
        children=f'There were **{line_item_count}** products sold with a total average revenue of $**{avg_revenue:.2f}**' 
    )
    total_clicks = dcc.Markdown(
        id='total-product-sales',
        children=f'There were **{line_item_count}** products sold with a total average revenue of $**{avg_revenue:.2f}**' 
    )
    main_div.children=[
            html.H1(children="Summary"),
            period,
            total_orders_by_period,
            total_line_items,
            total_clicks
        ]
    return main_div

