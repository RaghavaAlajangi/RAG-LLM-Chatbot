import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from dash import (
    Dash,
    Input,
    Output,
    State,
    _dash_renderer,
    callback,
    ctx,
    dcc,
    html,
)
from dotenv import load_dotenv

from .pages import chat_ui, login, logout, main, signup, upload
from .utils import get_login_reponse

load_dotenv()


_dash_renderer._set_react_version("18.2.0")

# Dash Bootstrap CSS URL
DBC_CSS = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap"
    "-templates@V1.0.1/dbc.min.css"
)

app = Dash(
    suppress_callback_exceptions=True,
    title="RAGbot",
    assets_folder="assets",
    external_stylesheets=[dbc.themes.DARKLY, DBC_CSS, dbc.icons.BOOTSTRAP],
)
app._favicon = "icon.svg"


app.layout = dmc.MantineProvider(
    [
        dcc.Location(id="app_url", refresh=False),
        dcc.Location(id="main_url", refresh=False),
        dcc.Store(id="user_token", storage_type="session"),
        html.Div(id="app_content"),
    ]
)


@callback(
    Output("login_status", "children"),
    Output("user_token", "data"),
    Input("login_button", "n_clicks"),
    State("user_email", "value"),
    State("user_password", "value"),
    prevent_initial_call=True,
)
def login_button_click(_, user_email, user_password):
    if ctx.triggered_id == "login_button" and user_email and user_password:
        resp = get_login_reponse(user_email.strip(), user_password.strip())
        if resp.status_code == 200:
            token = resp.json()["access_token"]
            return dcc.Location(href="/main", id="chatbot_link"), token
        return "Invalid Credentials", None
    return "", None


@callback(
    Output("app_content", "children"),
    Input("app_url", "pathname"),
)
def display_app_pages(pathname):
    if pathname == "/":
        return login.layout()
    elif pathname == "/logout":
        return logout.layout()
    elif pathname == "/signup":
        return signup.layout()
    else:
        return main.layout()


@callback(
    Output("page_content", "children"),
    Input("main_url", "pathname"),
)
def navigate_main_content(pathname):
    if pathname == "/main":
        return main.layout()
    elif pathname == "/database":
        return upload.layout()
    elif pathname == "/new_chat":
        return chat_ui.layout()
    else:
        return main.layout()
