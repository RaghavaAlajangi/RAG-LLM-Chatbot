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

from ..utils import fetch_chat, get_chat_response, get_model_list, update_chat

load_dotenv()


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


def layout(user_token, chat_id):
    PANEL_MAX_WIDTH = "800px"
    chat_msg_list = fetch_chat(user_token, chat_id)
    return dmc.Container(
        fluid=True,
        style={
            "minHeight": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
        },
        children=[
            dcc.Store(
                id="chat_msg_store",
                data=chat_msg_list,
                storage_type="session",
            ),
            dcc.Store(
                id="chat_id_store",
                data=chat_id,
                storage_type="session",
            ),
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
            ),
        ],
    )


clientside_callback(
    ClientsideFunction(namespace="clientside", function_name="enter_button"),
    Output("chat_submit_button", "n_clicks"),
    Input("chat_input_text", "n_submit"),
)


# Show user message and placeholder bot bubble
@callback(
    Output("chat_msg_store", "data"),
    Output("chat_input_text", "value"),
    Input("chat_submit_button", "n_clicks"),
    State("chat_input_text", "value"),
    State("chat_msg_store", "data"),
    prevent_initial_call=True,
)
def store_messages(n_clicks, user_message, cached_chat_msgs):
    if ctx.triggered_id == "chat_submit_button" and user_message:
        msg_idx = len(cached_chat_msgs) + 1
        cached_chat_msgs.append(
            {"role": "user", "content": user_message, "idx": msg_idx}
        )
        cached_chat_msgs.append(
            {"role": "assistant", "content": "__pending__", "idx": msg_idx}
        )
        return cached_chat_msgs, ""
    return cached_chat_msgs, ""


@callback(
    Output("chat_area", "children"),
    Input("chat_msg_store", "data"),
    prevent_initial_call=True,
)
def update_chat_area(cached_chat_msgs):
    return [
        chat_bubble(msg["content"], msg["role"], idx)
        for idx, msg in enumerate(cached_chat_msgs)
    ]


@callback(
    Output("chat_msg_store", "data", allow_duplicate=True),
    Input("chat_msg_store", "data"),
    Input("user_token", "data"),
    Input("chat_id_store", "data"),
    prevent_initial_call="initial_duplicate",
)
def stream_bot_response(cached_chat_msgs, user_token, cached_chat_id):
    model_name = get_model_list()[0]

    if len(cached_chat_msgs) > 0 and cached_chat_id is not None:
        bot_pending_msg = cached_chat_msgs[-1]["content"]

        if bot_pending_msg != "__pending__":
            return cached_chat_msgs

        response = get_chat_response(
            user_token, model_name, chat_history=cached_chat_msgs[:-1]
        )

        cached_chat_msgs[-1]["content"] = response["answer"]

        # Update the chat in the backend DB
        update_chat(
            user_token,
            cached_chat_id,
            cached_chat_msgs,
        )

        return cached_chat_msgs
    return cached_chat_msgs
