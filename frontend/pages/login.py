import dash_mantine_components as dmc
from dash import html


def layout():
    return html.Div(
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
                            html.Br(),
                            dmc.TextInput(
                                label="Email",
                                placeholder="Enter emial id",
                                id="user_email",
                            ),
                            dmc.PasswordInput(
                                label="Password",
                                placeholder="Enter password",
                                id="user_password",
                            ),
                            html.Br(),
                            dmc.Group(
                                [
                                    dmc.Button(
                                        "Login",
                                        id="login_button",
                                        color="#494646",
                                    )
                                ],
                                justify="center",
                            ),
                            html.Br(),
                            dmc.Text(
                                "Do not have an account?",
                                c="#494646",
                                style={"textAlign": "left"},
                            ),
                            dmc.Anchor(
                                "Sign Up",
                                href="/signup",
                                underline="always",
                                style={
                                    "textAlign": "left",
                                    "color": "black",
                                    "marginTop": "10px",
                                },
                            ),
                            html.Br(),
                            html.Br(),
                            html.Div(
                                id="login_status", style={"color": "red"}
                            ),
                        ],
                        disabled=False,
                        variant="default",
                        radius="md",
                        w="40%",
                    ),
                ],
            ),
        ],
    )
