import dash_mantine_components as dmc
from dash import Input, Output, callback, html, no_update
from dash_iconify import DashIconify


def logout_click():
    return html.Div(
        dmc.NavLink(
            label="Logout",
            href="/",
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
