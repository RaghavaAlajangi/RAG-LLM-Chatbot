import dash_mantine_components as dmc
from dash import Input, Output, State, callback, ctx, dcc, html

from ..utils import get_signup_response


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
                                "Sign UP",
                                order=1,
                                c="#494646",
                                style={"textAlign": "center"},
                            ),
                            dmc.TextInput(
                                label="Email",
                                placeholder="Enter email id",
                                id="signup_email",
                                required=True,
                            ),
                            dmc.PasswordInput(
                                label="Password",
                                placeholder="Enter password",
                                id="signup_password_1",
                                required=True,
                            ),
                            dmc.PasswordInput(
                                label="Re-enter Password",
                                placeholder="Enter password",
                                id="signup_password_2",
                                required=True,
                            ),
                            html.Br(),
                            dmc.Group(
                                [
                                    dmc.Button(
                                        "Sign Up",
                                        id="signup_button",
                                        color="#494646",
                                    )
                                ],
                                justify="center",
                            ),
                            html.Br(),
                            dmc.Anchor(
                                "Have an account? Login here!",
                                href="/",
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
                                children="",
                                id="show_signup_status",
                                style={"color": "red"},
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


@callback(
    Output("show_signup_status", "children"),
    Input("signup_button", "n_clicks"),
    State("signup_email", "value"),
    State("signup_password_1", "value"),
    State("signup_password_2", "value"),
    prevent_initial_call=True,
)
def signup_user(_, email, password1, password2):
    pre_email = email.strip()
    pre_pass_1 = password1.strip()
    pre_pass_2 = password2.strip()

    if ctx.triggered_id == "signup_button":
        if not pre_email or not pre_pass_1 or not pre_pass_2:
            return "All fields required."
        if pre_pass_1 != pre_pass_2:
            return "Passwords do not match."
        response = get_signup_response(pre_email, pre_pass_1)
        if response == 201:
            return dcc.Location(href="/", id="redirect_login")
        elif response == 400:
            return "Email already exists."
        return "Signup failed."
