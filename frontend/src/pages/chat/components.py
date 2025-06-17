import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify


def chat_bubble(message, sender="user", idx=0):
    """Renders a chat bubble with action icons."""
    # Common styles
    base_style = {
        "color": "#ececf1",  # Text color
        "padding": "16px",  # Padding inside the bubble
        "borderRadius": "12px",  # Rounded corners
        "maxWidth": "100%",  # Adjusted to 100%
        "marginBottom": "5px",  # Space between messages
        "fontFamily": "Monaco, monospace",
        "position": "relative",
        "boxShadow": "0 1.5px 4px 0 rgba(0,0,0,0.06)",  # Subtle shadow
        "whiteSpace": "pre-line",  # for multi-line messages
        "wordWrap": "break-word",  # Add this line
    }
    # Position and bg color
    if sender == "user":
        base_style.update(
            {
                "background": "#343541",  # User message background
                "marginLeft": "auto",
                "marginRight": 0,
                "width": "70%",  # Adjusted width for user messages
            }
        )
        icon_overlay = html.Div(
            [
                dmc.ActionIcon(
                    DashIconify(
                        icon="solar:copy-bold", color="#adadad", width=20
                    ),
                    variant="subtle",
                    size="lg",
                    style={"marginRight": "2px"},
                    id={"type": "copy_btn", "index": idx, "sender": sender},
                ),
                dmc.ActionIcon(
                    DashIconify(icon="tabler:edit", color="#adadad", width=20),
                    variant="subtle",
                    size="lg",
                    id={"type": "edit_btn", "index": idx, "sender": sender},
                ),
            ],
            style={
                "display": "flex",
                "gap": "2px",
                "justifyContent": "flex-end",  # Align icons to the right
                "alignItems": "flex-end",  # Align icons to the bottom
            },
        )
    else:
        base_style.update(
            {
                # "background": "#070716",  # Bot message background
                "marginLeft": 0,
                "marginRight": "auto",
            }
        )
        icon_overlay = html.Div(
            [
                dmc.ActionIcon(
                    DashIconify(
                        icon="solar:copy-bold", color="#adadad", width=20
                    ),
                    variant="subtle",
                    size="lg",
                    id={"type": "copy_btn", "index": idx, "sender": sender},
                ),
            ],
        )
    return html.Div(
        [
            html.Div(
                children=[html.Div(message)],
                style=base_style,
            ),
            icon_overlay,
            # html.Br(),
        ]
    )


def chat_input_box():
    return html.Div(
        [
            # Hidden div to simulate submit or store text if needed
            dcc.Store(id="input_submitted_text"),
            html.Div(
                [
                    dcc.Textarea(
                        id="chat_input_text",
                        placeholder="Ask anything",
                        style={
                            "flex": 1,
                            "background": "transparent",
                            "border": "none",
                            "outline": "none",
                            "color": "#ececf1",
                            "fontSize": "15px",
                            "resize": "none",  # Prevent manual resizing
                            "height": "100px",  # Adjust height
                            "overflow": "auto",
                        },
                        # autoFocus=True,
                    ),
                    html.Div(
                        dmc.ActionIcon(
                            DashIconify(
                                icon="majesticons:send",
                                color="#adadad",
                                width=40,
                            ),
                            variant="subtle",
                            size="lg",
                        ),
                        style={
                            "marginLeft": "10px",
                            "marginRight": "10px",
                            "marginTop": "8px",
                            "width": "28px",
                            "height": "28px",
                            "display": "flex",
                            "alignItems": "center",
                            "justifyContent": "center",
                            "fontSize": "22px",
                            "background": "#36373A",
                            "borderRadius": "50%",
                        },
                    ),
                ],
                style={
                    "width": "100%",
                    "display": "flex",
                    "alignItems": "center",
                },
            ),
        ],
        style={
            "width": "49%",
            "display": "flex",
            "height": "120px",
            "background": "#36373A",
            "borderRadius": "20px",
            "padding": "30px 40px",
            "position": "fixed",
            "bottom": 15,
            "left": "50%",
            "transform": "translateX(-31%)",
            "zIndex": 1,
        },
    )
