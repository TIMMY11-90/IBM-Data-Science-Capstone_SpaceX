# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
from dash import html
from dash import dcc


# Read the airline data into pandas dataframe
spacex_df = pd.read_csv(r"E:\FILE_SPACE_X\spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

# Get the list of launch sites
launch_sites = spacex_df["Launch Site"].unique().tolist()
launch_sites.insert(0, "ALL")

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        dcc.Dropdown(
            id="site-dropdown",
            options=[{"label": i, "value": i} for i in launch_sites],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
        ),
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value"),
)
def update_pie_chart(selected_site):
    if selected_site == "ALL":
        fig = px.pie(
            spacex_df,
            values="class",
            names="Launch Site",
            title="Total Success Launches By Site",
        )
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == selected_site]
        fig = px.pie(
            filtered_df,
            names="class",
            title="Total Success Launches for site {}".format(selected_site),
        )
    return fig


# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value"),
    ],
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    mask = (spacex_df["Payload Mass (kg)"] > low) & (
        spacex_df["Payload Mass (kg)"] < high
    )

    if selected_site == "ALL":
        fig = px.scatter(
            spacex_df[mask],
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for all Sites",
        )
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == selected_site]
        fig = px.scatter(
            filtered_df[mask],
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for {}".format(
                selected_site
            ),
        )
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server()
