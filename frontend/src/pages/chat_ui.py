import dash_mantine_components as dmc
from dash import html

from .chat.components import chat_bubble, chat_input_box

dummy_chats = [
    {"sender": "user", "text": "Hello, who are you?"},
    {
        "sender": "bot",
        "text": "I'm an AI assistant here to help with your questions!",
    },
    {
        "sender": "user",
        "text": "Can you write Python code for Fibonacci?",
    },
]


def layout():
    return dmc.Container(
        fluid=True,
        style={
            "minHeight": "100vh",
            "padding": 0,
            "fontFamily": "Inter, 'Segoe UI', Arial, sans-serif",
            "display": "flex",  # Use flexbox for layout
            "justifyContent": "center",  # Center horizontally
            "alignItems": "center",  # Center vertically
        },
        children=[
            html.Div(
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "minHeight": "80vh",  # Reduced height
                    "position": "relative",
                    "width": "60%",  # Match chat input width
                },
                children=[
                    # Chat messages area
                    html.Div(
                        id="chat-history",
                        style={
                            "flexGrow": 1,
                            "overflowY": "auto",
                            "padding": "36px 0px",
                        },
                        children=[
                            chat_bubble(msg["text"], msg["sender"], idx)
                            for idx, msg in enumerate(dummy_chats)
                        ],
                    ),
                    # Input bar
                    chat_input_box(),
                ],
            ),
        ],
    )
