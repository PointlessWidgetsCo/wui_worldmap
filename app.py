import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import datetime

# Load the Excel dataset
df = pd.read_excel("WUI M Dataset Apr 2025.xlsx", sheet_name="T1")

# Prepare data
df_long = df.melt(id_vars=['date'], var_name='Country', value_name='Uncertainty')
df_long['Month'] = df_long['date'].dt.strftime('%Y-%m')
months = df_long['Month'].unique()

min_value = df_long['Uncertainty'].min()
max_value = 1.3

# Prepare each frame by month
frame_dict = {}
for month in months:
    month_data = df_long[df_long['Month'] == month]
    frame_dict[month] = go.Choropleth(
        locations=month_data['Country'],
        z=month_data['Uncertainty'],
        text=month_data['Country'],
        hoverinfo="location+z+text",
        colorscale="RdYlBu_r",
        zmin=min_value,
        zmax=max_value,
        colorbar=dict(title="Uncertainty")
    )

# Initialize Dash app
app = Dash(__name__)
app.title = "IMF Uncertainty Index"

app.layout = html.Div([
    html.H2("IMF World Uncertainty Index by Country"),
    dcc.Graph(id='choropleth-map'),
    html.Div([
        html.Button("Play", id='play-button'),
        dcc.Slider(
            id='month-slider',
            min=0,
            max=len(months)-1,
            step=1,
            value=0,
            marks={i: m for i, m in enumerate(months)},
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ], style={"width": "90%", "margin": "auto"}),
    dcc.Interval(id="interval", interval=2000, n_intervals=0, disabled=True),
    html.Div("Source: https://worlduncertaintyindex.com/", style={"textAlign": "center", "marginTop": 40})
])

@app.callback(
    Output("choropleth-map", "figure"),
    Input("month-slider", "value")
)
def update_figure(selected_index):
    month = months[selected_index]
    choropleth = frame_dict[month]
    fig = go.Figure(data=[choropleth])
    fig.update_layout(
        geo=dict(showcoastlines=True, coastlinecolor="Black", projection_type="natural earth"),
        annotations=[dict(
            text=pd.to_datetime(month).strftime("%B %Y"),
            x=0.5, y=0.18,
            xref="paper", yref="paper",
            font=dict(size=36, color="black"),
            showarrow=False,
            xanchor="center"
        )]
    )
    return fig

@app.callback(
    Output("interval", "disabled"),
    Input("play-button", "n_clicks"),
    prevent_initial_call=True
)
def start_animation(n_clicks):
    return False  # enable animation

@app.callback(
    Output("month-slider", "value"),
    Input("interval", "n_intervals"),
    Input("month-slider", "value")
)
def advance_slider(n_intervals, current_index):
    if current_index >= len(months) - 1:
        return 0  # restart loop
    return current_index + 1

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
