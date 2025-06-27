import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify


def layout():
    return html.Div(
        [
            dmc.Container(
                fluid=True,
                style={
                    "display": "flex",
                    "flexDirection": "column",  # Stack children vertically
                    "justifyContent": "left",
                    "alignItems": "left",
                    # Ensure it takes at least the full viewport height
                    "minHeight": "80vh",
                    "color": "gray",
                    "borderRadius": "8px",
                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)",
                    "padding": "20px",
                },
                children=[
                    dmc.Text("Update Vector Database:", c="white", size="xl"),
                    html.Div(
                        "Upload your files to the vector database. Supported "
                        "formats: PDF, DOCX, TXT, and HTML.",
                        style={"marginTop": "10px", "color": "lightgray"},
                    ),
                    # dcc.Upload(
                    #     id="upload_data",
                    #     children=html.Div(
                    #         [
                    #             DashIconify(
                    #                 icon="solar:upload-broken",
                    #                 width=20,
                    #                 color="#ececf1",
                    #             ),
                    #             html.Span(
                    #                 "  Upload file", style={"marginLeft": 8}
                    #             ),
                    #         ]
                    #     ),
                    #     style={
                    #         "width": "50%",
                    #         "border": "1px dashed #40414f",
                    #         "borderRadius": "8px",
                    #         "background": "#242428",
                    #         "color": "#ececf1",
                    #         "alignItems": "center",
                    #         "display": "flex",
                    #         "padding": "12px",
                    #         "cursor": "pointer",
                    #         "fontSize": "15px",
                    #         "marginBottom": "10px",
                    #     },
                    #     multiple=True,
                    # ),
                    dcc.Upload(
                        id="upload_data",
                        children=html.Div(
                            [
                                "Drag and Drop or ",
                                html.A("Select Files"),
                            ]
                        ),
                        style={
                            "width": "50%",
                            "height": "60px",
                            "lineHeight": "60px",
                            "borderWidth": "1px",
                            "borderStyle": "dashed",
                            "borderRadius": "5px",
                            "textAlign": "center",
                            "marginTop": "10px",
                            "marginBottom": "10px",
                            "color": "#9DA3AA",
                        },
                        # Allow multiple files to be uploaded
                        multiple=True,
                    ),
                    dmc.Button(
                        "Process",
                        id="process_button",
                        variant="outline",
                        disabled=False,
                        size="sm",
                        color="#9DA3AA",
                        rightSection=DashIconify(icon="uim:process", width=20),
                        style={
                            "width": "120px",
                        },
                    ),
                ],
            ),
        ]
    )
