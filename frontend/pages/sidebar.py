import dash_mantine_components as dmc
from dash import Input, Output, State, callback, dcc, html
from dash_iconify import DashIconify

from ..utils import get_chat_list, get_current_user
from .logout import logout_click


def sidebar_layout():
    """Creates the sidebar layout for the dashboard."""

    return html.Div(
        children=[
            # Sidebar toggle button
            html.Button(
                DashIconify(icon="cuida:sidebar-collapse-outline"),
                id="sidebar_toggle",
                style={
                    "position": "absolute",
                    "top": "15px",
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
            # Menu links
            html.Div(
                [
                    # Database link
                    dmc.NavLink(
                        label="Database",
                        href="/database",
                        leftSection=DashIconify(
                            icon="mdi:database-outline",
                            width=20,
                        ),
                        variant="subtle",
                        color="white",
                        active="partial",
                    ),
                    # New Chat link
                    dmc.NavLink(
                        label="Chat",
                        href="/new_chat",
                        leftSection=DashIconify(
                            icon="bx:chat",
                            width=20,
                        ),
                        variant="subtle",
                        color="white",
                        active="partial",
                    ),
                    html.Hr(
                        style={
                            "borderColor": "white",
                        }
                    ),
                    # History section
                    dmc.Text(
                        "History", c="white", style={"marginLeft": "10px"}
                    ),
                    html.Br(),
                    dmc.ScrollArea(
                        h=500,
                        # w=350,
                        children=[
                            html.Div(
                                id="chat_history_list",
                            )
                        ],
                    ),
                ],
                style={
                    "margin-bottom": "20px",
                    "left": "0px",
                },
            ),
            # User Logout section
            html.Div(
                [
                    html.Hr(
                        style={
                            "borderColor": "white",
                            "width": "100%",
                        }
                    ),
                    html.Div(
                        id="logout_status",
                        style={
                            "margin-bottom": "10px",
                        },
                    ),
                ],
                style={
                    "position": "absolute",
                    "bottom": "20px",
                    "left": "20px",
                    "width": "calc(100% - 40px)",
                },
            ),
        ],
        id="sidebar",
        style={
            "height": "100%",
            "width": "20rem",
            "position": "fixed",
            "top": 0,
            "left": 0,
            "overflow-x": "hidden",
            "padding": "20px",
            "background-color": "#1c1919",
            "color": "white",
        },
    )


@callback(
    Output("logout_status", "children"),
    Input("user_token", "data"),
)
def show_user(user_token):
    user_data = get_current_user(user_token)
    if user_data:
        return [
            dmc.Avatar(
                name=user_data["email"],
                color="initials",
                variant="outline",
                style={"margin-left": "10px"},
            ),
            logout_click(),
        ]
    return dcc.Location(href="/", id="redirect_to_login")


@callback(
    Output("chat_history_list", "children"),
    Input("user_token", "data"),
    State("chat_history_list", "children"),
)
def show_chat_history_links(user_token, chat_history_list):
    # Note: this api call can be removed if chat_list is cached
    chat_list = get_chat_list(user_token)
    if chat_list:
        return [
            dmc.NavLink(
                label=chat["title"] or "Untitled Chat",
                href=f"/chat/{chat['id']}",
                leftSection=DashIconify(icon="tabler:gauge"),
                rightSection=DashIconify(icon="tabler-chevron-right"),
                style={
                    "color": "gray",
                    "text-decoration": "red",
                },
                # variant="subtle",
                # color="white",
                active="partial",
            )
            for chat in chat_list
        ]
    return chat_history_list


# @callback(
#     Output("sidebar", "style"),
#     Output("page_content", "style"),
#     Input("sidebar_toggle", "n_clicks"),
#     State("sidebar", "style"),
#     State("page_content", "style"),
#     prevent_initial_call=True,
# )
# def toggle_sidebar(n_clicks, sidebar_style, page_content_style):
#     if n_clicks:
#         collapsed = sidebar_style.get("width") == "6rem"
#         new_sidebar_width = "25rem" if collapsed else "6rem"
#         new_margin_left = "25rem" if collapsed else "6rem"

#         sidebar_style["width"] = new_sidebar_width
#         page_content_style["margin-left"] = new_margin_left

#         return sidebar_style, page_content_style
#     else:
#         return sidebar_style, page_content_style
