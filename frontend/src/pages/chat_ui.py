import os

import dash_mantine_components as dmc
import feffery_markdown_components as fmc
from dash import (
    ClientsideFunction,
    Input,
    Output,
    State,
    callback,
    clientside_callback,
    ctx,
    dcc,
    html,
)
from dash_iconify import DashIconify
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

sys_prompt = {"role": "system", "content": "You are a helpful assistant."}

api_key = os.environ.get("GWDG_API_KEY")
base_url = os.environ.get("GWDG_ENDPOINT")
model_name = os.environ.get("GWDG_MODEL_NAME")
client = OpenAI(api_key=api_key, base_url=base_url)


def get_llm_response(message_list):
    """Get LLM model response."""
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=message_list,
            stream=True,
        )
        return response
    except Exception as e:
        return f"Error: {str(e)}"


def chat_bubble(message, role="user", idx=0):
    base_style = {
        "width": "100%",
        "color": "#ececf1",
        "padding": "16px",
        "borderRadius": "12px",
        "maxWidth": "100%",
        "marginBottom": "5px",
        "fontFamily": "Monaco, monospace",
        "position": "relative",
        "whiteSpace": "pre-line",
        # Keep the text (quiry and response) in desired space
        "wordWrap": "break-word",
        "wordBreak": "break-word",
        "overflowWrap": "break-word",
        "boxSizing": "border-box",
    }

    if role == "user":
        base_style.update(
            {
                "background": "#343541",
                "marginLeft": "auto",
                "marginRight": 0,
                "width": "70%",
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
                "justifyContent": "flex-end",
            },
        )
        return html.Div(
            [html.Div(html.Div(message), style=base_style), icon_overlay]
        )

    else:
        base_style.update(
            {
                "background": "transparent",
                # "background": "#343541",
                "marginLeft": 0,
                "marginRight": "auto",
            }
        )
        if message == "__pending__":
            message_format = dmc.Group(
                [
                    dmc.Loader(
                        color="white",
                        size="xs",
                        type="oval",
                    ),
                    dmc.Text(
                        "Thinking..",
                    ),
                ],
                align="center",
            )
            icon_overlay = None
        else:
            message_format = fmc.FefferyMarkdown(
                markdownStr=message,
                codeTheme="coldark-dark",
                style={
                    "color": "#ececf1",
                    "wordBreak": "break-word",
                    "background": "transparent",
                },
                className="table-scrollable",
            )

            icon_overlay = dmc.Group(
                [
                    dmc.ActionIcon(
                        DashIconify(
                            icon="solar:copy-bold", color="#adadad", width=20
                        ),
                        variant="subtle",
                        size="lg",
                        id={"type": "copy_btn", "index": idx, "sender": role},
                    ),
                    dmc.ActionIcon(
                        DashIconify(
                            icon="prime:thumbs-up-fill",
                            color="#adadad",
                            width=24,
                        ),
                        variant="subtle",
                        size="lg",
                        id={
                            "type": "thumbup_btn",
                            "index": idx,
                            "sender": role,
                        },
                    ),
                    dmc.ActionIcon(
                        DashIconify(
                            icon="prime:thumbs-down-fill",
                            color="#adadad",
                            width=24,
                        ),
                        variant="subtle",
                        size="lg",
                        id={
                            "type": "thumbdown_btn",
                            "index": idx,
                            "sender": role,
                        },
                    ),
                ],
                align="center",
                gap="xs",
            )

        return html.Div(
            [html.Div(message_format, style=base_style), icon_overlay]
        )


def chat_input_box(input_id, submit_id, panel_max_width):
    return html.Div(
        [
            dcc.Store(id="chat_store", data=[]),
            dmc.Paper(
                dmc.Textarea(
                    id=input_id,
                    placeholder="Ask anything...",
                    minRows=1,
                    maxRows=4,
                    autosize=True,
                    radius="md",
                    persistence=True,
                    rightSection=dmc.Center(
                        dmc.ActionIcon(
                            DashIconify(icon="fluent:send-16-filled"),
                            color="#adadad",
                            id=submit_id,
                        )
                    ),
                    style={
                        "overflow": "hidden",
                        "width": "100%",
                        "boxSizing": "border-box",
                    },
                ),
                radius="lg",
                p="xs",
                style={
                    "maxWidth": panel_max_width,
                    "width": "100%",
                    "height": "120px",
                    "backgroundColor": "#3a3b3b",
                    "borderRadius": "20px",
                    "padding": "30px 40px",
                    "position": "fixed",
                    "bottom": 15,
                    "zIndex": 1000,
                    "display": "flex",
                    "alignItems": "center",
                },
            ),
        ]
    )


def layout():
    PANEL_MAX_WIDTH = "800px"
    return dmc.Container(
        fluid=True,
        style={
            "minHeight": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
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
                    html.Br(),
                    dmc.ScrollArea(
                        id="chat_area",
                        type="hover",
                        scrollbarSize=2,
                        offsetScrollbars=True,
                        style={
                            "paddingBottom": "200px",
                            "overflowX": "hidden",
                            "maxWidth": PANEL_MAX_WIDTH,
                            "width": "100%",
                        },
                        children=[],
                    ),
                    chat_input_box(
                        "chat_input_text",
                        "chat_submit_button",
                        PANEL_MAX_WIDTH,
                    ),
                ],
            )
        ],
    )


clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="enter_button"),
    Output("chat_submit_button", "n_clicks"),
    Input("chat_input_text", "n_submit"),
)


# Show user message and placeholder bot bubble
@callback(
    Output("chat_store", "data"),
    Output("chat_input_text", "value"),
    Input("chat_submit_button", "n_clicks"),
    State("chat_input_text", "value"),
    State("chat_store", "data"),
    prevent_initial_call=True,
)
def store_messages(n_clicks, user_message, chat_messages):
    if ctx.triggered_id == "chat_submit_button" and user_message:
        msg_idx = len(chat_messages) + 1
        chat_messages.append(
            {"sender": "user", "content": user_message, "idx": msg_idx}
        )
        chat_messages.append(
            {"sender": "bot", "content": "__pending__", "idx": msg_idx}
        )
        return chat_messages, ""
    return chat_messages, ""


# Render chat bubbles
@callback(
    Output("chat_area", "children"),
    Input("chat_store", "data"),
    prevent_initial_call=True,
)
def update_chat_area(chat_messages):
    return [
        chat_bubble(msg["content"], msg["sender"], msg["idx"])
        for msg in chat_messages
    ]


# Background streaming bot response
@callback(
    Output("chat_store", "data", allow_duplicate=True),
    Input("chat_store", "data"),
    prevent_initial_call="initial_duplicate",
)
def stream_bot_response(chat_messages):
    # Find the latest pending message
    for i in range(len(chat_messages) - 1, -1, -1):
        if (
            chat_messages[i]["sender"] == "bot"
            and chat_messages[i]["content"] == "__pending__"
        ):
            user_message = chat_messages[i - 1]["content"] if i > 0 else ""
            sys_prompt = "you are a helpful assistant."
            try:
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": sys_prompt},
                        {"role": "user", "content": user_message},
                    ],
                    stream=True,
                )
                full_response = ""
                for chunk in response:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                chat_messages[i]["content"] = full_response
                break
            except Exception as e:
                chat_messages[i]["content"] = f"Error: {str(e)}"
                break
    return chat_messages
