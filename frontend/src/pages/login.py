import dash
import dash_mantine_components as dmc
from dash import html

dash.register_page(__name__, path="/")

# Login screen
layout = html.Div(
    children=[
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
                            "Login to RAGbot",
                            order=1,
                            c="#494646",
                            style={"textAlign": "center"},
                        ),
                        dmc.TextInput(
                            label="Username",
                            placeholder="Enter username",
                            id="uname-box",
                        ),
                        dmc.PasswordInput(
                            label="Password",
                            placeholder="Enter password",
                            id="pwd-box",
                        ),
                        html.Br(),
                        dmc.Group(
                            [dmc.Button("Login", id="login-button")],
                            justify="center",
                        ),
                    ],
                    disabled=False,
                    variant="default",
                    radius="md",
                    w="40%",
                ),
            ],
        ),
        html.Div(children="", id="output-state"),
    ],
)
