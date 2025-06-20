import os

import dash
import dash_mantine_components as dmc
import feffery_markdown_components as fmc
from dash import ClientsideFunction, Input, Output, State, ctx, dcc, html
from dash_iconify import DashIconify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.environ.get("GWDG_API_KEY")
base_url = os.environ.get("GWDG_ENDPOINT")
model_name = os.environ.get("GWDG_MODEL_NAME")
client = OpenAI(api_key=api_key, base_url=base_url)


def get_llm_response(user_message):
    """Get LLM model response."""
    try:
        completion = client.completions.create(
            model=model_name,
            prompt=user_message,
            max_tokens=512,
        )
        return completion.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def chat_bubble(message, role="user", idx=0):
    """Renders a chat bubble with action icons."""
    # Common styles
    base_style = {
        "width": "100%",
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
    if role == "user":
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
                    id={"type": "copy_btn", "index": idx, "sender": role},
                ),
                dmc.ActionIcon(
                    DashIconify(icon="tabler:edit", color="#adadad", width=20),
                    variant="subtle",
                    size="lg",
                    id={"type": "edit_btn", "index": idx, "sender": role},
                ),
            ],
            style={
                "display": "flex",
                "gap": "2px",
                "justifyContent": "flex-end",  # Align icons to the right
                "alignItems": "flex-end",  # Align icons to the bottom
            },
        )
        # message_format = html.Div(message)
        message_format = dcc.Markdown(message)
    else:
        base_style.update(
            {
                # "background": "#070716",  # Bot message background
                "background": "transparent",
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
                    id={"type": "copy_btn", "index": idx, "sender": role},
                ),
            ],
        )
        message_format = fmc.FefferyMarkdown(
            markdownStr=message,
            codeTheme="coldark-dark",  # consistent dark code theme
            style={"color": "#ececf1", "background": "transparent"},
        )
        # message_format = html.Div(message)
        # message_format = dcc.Markdown(message)
    return html.Div(
        [
            html.Div(
                children=[message_format],
                style=base_style,
            ),
            icon_overlay,
        ]
    )


def chat_input_box(input_id, submit_id, panel_max_width):
    return html.Div(
        [
            dcc.Store(id="chat_store", data=[]),
            html.Div(
                [
                    dcc.Textarea(
                        id=input_id,
                        placeholder="Ask anything",
                        style={
                            "flex": 1,
                            "background": "transparent",
                            "border": "none",
                            "outline": "none",
                            "color": "#ececf1",
                            "fontSize": "15px",
                            "resize": "none",
                            "height": "100px",
                            "overflow": "auto",
                        },
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
                            id=submit_id,
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
            "maxWidth": panel_max_width,  # Match parent chat panel
            "width": "100%",
            "display": "flex",
            "height": "120px",
            "background": "#36373A",
            "borderRadius": "20px",
            "padding": "30px 40px",
            "boxSizing": "border-box",
            "position": "fixed",
            "bottom": 15,
            "alignItems": "center",
            "zIndex": 1000,
        },
    )


def layout():
    # Shared panel style for both chat history and chat input box
    PANEL_MAX_WIDTH = "800px"

    return dmc.Container(
        fluid=True,
        style={
            "minHeight": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            # Sidebar or more outer layout goes here if needed
        },
        children=[
            html.Div(
                style={
                    "position": "relative",
                    "maxWidth": PANEL_MAX_WIDTH,
                    "width": "100%",
                    "margin": "0 auto",
                },
                children=[
                    dmc.ScrollArea(
                        id="chat_area",
                        type="hover",
                        scrollbarSize=4,
                        offsetScrollbars=True,
                        style={
                            "paddingBottom": "200px",
                        },
                        children=[],
                    ),
                    chat_input_box(
                        input_id="chat_input_text",
                        submit_id="chat_submit_button",
                        panel_max_width=PANEL_MAX_WIDTH,
                    ),
                ],
            ),
        ],
    )


dash.clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="enter_button"),
    Output("chat_submit_button", "n_clicks"),
    [Input("chat_input_text", "n_submit")],
)


@dash.callback(
    Output("chat_store", "data"),
    Output("chat_input_text", "value"),
    Input("chat_submit_button", "n_clicks"),
    State("chat_input_text", "value"),
    State("chat_store", "data"),
    prevent_initial_call=True,
)
def store_messages(n_clicks, user_message, chat_messages):
    if ctx.triggered_id == "chat_submit_button" and user_message:
        # Add user message to chat
        chat_messages.append({"sender": "user", "text": user_message})

        llm_response = get_llm_response(user_message)

        # Add bot message to chat
        chat_messages.append({"sender": "bot", "text": llm_response})

        return chat_messages, ""

    return chat_messages, ""


@dash.callback(
    Output("chat_area", "children"),
    Input("chat_store", "data"),
)
def update_chat_history(chat_messages):
    return [
        chat_bubble(msg["text"], msg["sender"], idx)
        for idx, msg in enumerate(chat_messages)
    ]
