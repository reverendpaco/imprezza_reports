import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from app import (
    app,
)  # ugly, but necessary, see: https://stackoverflow.com/questions/62102453/how-to-define-callbacks-in-separate-files-plotly-dash
import revenue
import cost
import pixel
import summary
import sql_util


SIMPLE_DISPATCH = {
    "/": summary.serve_summary,
    "/cost": cost.serve_cost,
    "/revenue": revenue.serve_revenue,
    "/pixel": pixel.serve_pixel,
}


def init_main_page():
    # the style arguments for the sidebar. We use position:fixed and a fixed width
    SIDEBAR_STYLE = {
        "position": "fixed",
        "top": 0,
        "left": 0,
        "bottom": 0,
        "width": "16rem",
        "padding": "2rem 1rem",
        "background-color": "#f8f9fa",
    }

    # the styles for the main content position it to the right of the sidebar and
    # add some padding.
    CONTENT_STYLE = {
        "margin-left": "18rem",
        "margin-right": "2rem",
        "padding": "2rem 1rem",
    }

    sidebar = html.Div(
        [
            html.H2("Cost/Revenue", className="display-12"),
            html.Hr(),
            # html.P(
            #     "–", className="lead"
            # ),
            dbc.Nav(
                [
                    dbc.NavLink("Summary", href="/", active="exact"),
                    dbc.NavLink("Cost By...", href="/cost", active="exact"),
                    dbc.NavLink("Revenue By...", href="/revenue", active="exact"),
                    dbc.NavLink("Pixel Events", href="/pixel", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        style=SIDEBAR_STYLE,
    )

    content = html.Div(id="page-content", style=CONTENT_STYLE)

    app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


def bad():
    return html.P("URL not recognized")


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    return SIMPLE_DISPATCH.get(pathname, bad)()


if __name__ == "__main__":
    sql_util.assert_db()
    init_main_page()
    app.run_server(port=8888)
