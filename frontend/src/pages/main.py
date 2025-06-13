import dash
import dash_mantine_components as dmc
from dash import Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

dash.register_page(__name__)


def line_breaks(times=1):
    return html.Br()


def sidebar_layout():
    """Creates the sidebar layout for the dashboard."""

    return html.Div(
        children=[
            # Sidebar toggle button
            html.Button(
                "☰",
                id="sidebar-toggle",
                style={
                    "position": "absolute",
                    "top": "10px",
                    "right": "10px",
                    "zIndex": "1000",
                    "backgroundColor": "transparent",
                    "border": "none",
                    "color": "white",
                    "fontSize": "24px",
                    "cursor": "pointer",
                },
            ),
            # Dashboard title
            html.Div(
                [
                    dmc.Group(
                        [
                            dmc.Image(src="assets/icon.svg", h=30),
                            dmc.Title("RAGbot", c="white", order=2),
                        ],
                        grow=False,
                    ),
                    html.Hr(
                        style={
                            "borderColor": "white",
                        }
                    ),
                ],
                style={
                    "position": "absolute",
                    "top": "20px",
                    "left": "20px",
                    "width": "calc(100% - 40px)",
                },
            ),
            html.Br(),
            html.Br(),
            html.Br(),
            dmc.NavLink(
                label="Database",
                leftSection=DashIconify(icon="octicon:database-16"),
                children=[
                    html.Div(
                        style={
                            "display": "flex",
                            "align-items": "flex-end",
                            "gap": "5px",  # Space between items
                        },
                        children=[
                            dcc.Upload(
                                id="upload-data",
                                children=html.Div(
                                    [
                                        "Drag and Drop or ",
                                        html.A("Select Files"),
                                    ]
                                ),
                                style={
                                    "width": "100%",
                                    "height": "60px",
                                    "lineHeight": "60px",
                                    "borderWidth": "1px",
                                    "borderStyle": "dashed",
                                    "borderRadius": "5px",
                                    "textAlign": "center",
                                    "margin": "10px",
                                },
                                # Allow multiple files to be uploaded
                                multiple=True,
                            ),
                            dmc.Button(
                                "Fetch",
                                id="scrape_click",
                                variant="outline",
                                disabled=False,
                                rightSection=DashIconify(
                                    icon="mdi:download-circle"
                                ),
                            ),
                            html.Div(id="notifications_container"),
                        ],
                    ),
                ],
            ),
            # Chat history
            html.Div(
                [
                    dmc.Text("History", c="gray"),
                    html.Br(),
                    dmc.ScrollArea(
                        h=500,
                        # w=350,
                        children=[
                            html.Div(
                                [
                                    dmc.NavLink(
                                        label=f"Chat {i+1}",
                                        href=f"#{i+1}",
                                        leftSection=DashIconify(
                                            icon="tabler:gauge"
                                        ),
                                        rightSection=DashIconify(
                                            icon="tabler-chevron-right"
                                        ),
                                        # autoContrast=True,
                                        color="red",
                                        style={
                                            "color": "gray",
                                            "text-decoration": "red",
                                        },
                                    )
                                    for i in range(100)
                                ],
                            )
                        ],
                    ),
                ],
                style={
                    "margin-bottom": "20px",
                    "left": "0px",
                },
            ),
            # User Login and settings
            html.Div(
                [
                    html.Hr(
                        style={
                            "borderColor": "white",
                            "width": "100%",
                        }
                    ),
                    html.Div(
                        id="user_login_status",
                        style={
                            "margin-bottom": "10px",
                        },
                    ),
                ],
                style={
                    "position": "absolute",
                    "bottom": "60px",
                    "left": "20px",
                    "width": "calc(100% - 40px)",
                },
            ),
        ],
        id="sidebar",
        style={
            "height": "100%",
            "width": "25rem",
            "position": "fixed",
            "top": 0,
            "left": 0,
            "overflow-x": "hidden",
            "padding": "20px",
            "background-color": "#1c1919",
            "color": "white",
        },
    )


layout = html.Div(
    [
        sidebar_layout(),
        dcc.Location(id="url", refresh=False),
        html.Div(
            id="page-content",
            style={
                "align-items": "center",
                "overflowX": "hidden",
                "margin-left": "20rem",
            },
        ),
    ]
)


@callback(
    [Output("sidebar", "style"), Output("page-content", "style")],
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "style"), State("page-content", "style")],
    prevent_initial_call=True,
)
def toggle_sidebar(n_clicks, sidebar_style, page_content_style):
    if n_clicks:
        collapsed = sidebar_style.get("width") == "6rem"
        new_sidebar_width = "25rem" if collapsed else "6rem"
        new_margin_left = "25rem" if collapsed else "6rem"

        sidebar_style["width"] = new_sidebar_width
        page_content_style["margin-left"] = new_margin_left

        return sidebar_style, page_content_style
    else:
        return sidebar_style, page_content_style
