import json
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Load figure from JSON
with open("fig_with_frames_for_dash.json") as f:
    fig_dict = json.load(f)
fig = go.Figure(fig_dict)

# Initialize Dash app
app = Dash(__name__)
app.title = "IMF Uncertainty Index"

app.layout = html.Div([
    dcc.Graph(figure=fig),
    html.Div("Source: https://worlduncertaintyindex.com/", style={"textAlign": "center", "marginTop": 20})
])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
