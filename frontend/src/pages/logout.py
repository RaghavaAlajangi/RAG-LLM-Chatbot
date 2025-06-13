import dash
import dash_mantine_components as dmc
from dash import dcc, html
from flask_login import current_user, logout_user

dash.register_page(__name__)


def layout():
    if current_user.is_authenticated:
        logout_user()
    return html.Div(
        [
            dmc.Container(
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "center",
                    "minHeight": "80vh",
                    "color": "gray",
                    "borderRadius": "8px",
                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
                },
                children=[
                    dmc.Fieldset(
                        children=[
                            dmc.Title(
                                "You have been logged out",
                                order=2,
                                c="#494646",
                                style={"textAlign": "center"},
                            ),
                            dmc.Title(
                                "Login Again?",
                                order=3,
                                c="#494646",
                                style={"textAlign": "center"},
                            ),
                            dcc.Link("Login", href="/"),
                        ],
                        disabled=False,
                        variant="default",
                        radius="md",
                        w="40%",
                    ),
                ],
            ),
        ]
    )
