import os

import dash
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

# from dash import callback_context as ctx
from dash import (
    Dash,
    Input,
    Output,
    State,
    _dash_renderer,
    callback,
    dcc,
    html,
)
from dash_iconify import DashIconify
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager, UserMixin, current_user, login_user

from .credentials import VALID_USERNAME_PASSWORD

load_dotenv()

# Exposing the Flask Server to enable configuring it for logging in
server = Flask(__name__)

_dash_renderer._set_react_version("18.2.0")

# Dash Bootstrap CSS URL
DBC_CSS = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap"
    "-templates@V1.0.1/dbc.min.css"
)

app = Dash(
    use_pages=True,
    server=server,
    suppress_callback_exceptions=True,
    title="RAGbot",
    assets_folder="assets",
    external_stylesheets=[dbc.themes.DARKLY, DBC_CSS, dbc.icons.BOOTSTRAP],
)
app._favicon = "icon.svg"

server.config.update(SECRET_KEY=os.getenv("SECRET_KEY"))

# Login manager object will be used to login / logout users
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = "/"


class User(UserMixin):
    # User data model. It has to have at least self.id as a minimum
    def __init__(self, username):
        self.id = username


@login_manager.user_loader
def load_user(username):
    """This function loads the user by user id. Typically this looks up the
    user from a user database. We won't be registering or looking up users
    in this example, since we'll just login using LDAP server. So we'll
    simply return a User object with the passed in username.
    """
    return User(username)


app.layout = dmc.MantineProvider(
    [
        dcc.Location(id="ref_url"),
        dash.page_container,
    ]
)


@callback(
    Output("user_status", "children"),
    Input("ref_url", "pathname"),
)
def update_authentication_status(_):
    if current_user.is_authenticated:
        return (
            html.A(
                [
                    DashIconify(
                        icon="tabler:logout",
                        style={"marginRight": "5px", "color": "white"},
                    ),
                    "Logout",
                ],
                href="/logout",
                style={
                    "color": "white",
                    "textDecoration": "none",
                    "fontSize": "16px",
                    "display": "flex",
                    "alignItems": "center",
                },
            ),
        )
    return dcc.Location(href="/", id="login_link")


@callback(
    Output("output-state", "children"),
    Input("login-button", "n_clicks"),
    State("uname-box", "value"),
    State("pwd-box", "value"),
    prevent_initial_call=True,
)
def login_button_click(n_clicks, username, password):
    if n_clicks > 0:
        if VALID_USERNAME_PASSWORD.get(username) is None:
            return "Invalid Username"
        if VALID_USERNAME_PASSWORD.get(username) == password:
            login_user(User(username))
            return dcc.Location(href="/main", id="chatbot_link")
        return "Invalid Credentials"
