import dash_mantine_components as dmc
from dash import Input, Output, callback, html, no_update
from dash_iconify import DashIconify


def layout():
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
                                style={"textAlign": "left"},
                            ),
                            dmc.Anchor(
                                "Login again?",
                                href="/",
                                underline="always",
                                style={
                                    "textAlign": "left",
                                    "color": "black",
                                    "marginTop": "10px",
                                },
                            ),
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


def logout_click():
    return html.Div(
        dmc.NavLink(
            label="Logout",
            href="/logout",
            leftSection=DashIconify(
                icon="tabler:logout",
                width=20,
            ),
            variant="subtle",
            color="white",
            active="partial",
        ),
    )


@callback(
    Output("user_token", "data", allow_duplicate=True),
    Input("app_url", "pathname"),
    prevent_initial_call=True,
)
def clear_token_on_logout(pathname):
    if pathname == "/logout":
        return None
    return no_update
