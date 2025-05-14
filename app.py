import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Load and prepare data
df = pd.read_excel("WUI M Dataset Apr 2025.xlsx", sheet_name="T1")
df_long = df.melt(id_vars=["date"], var_name="Country", value_name="Uncertainty")
df_long["Month"] = df_long["date"].dt.strftime("%Y-%m")

# Plotly Express animated choropleth
fig = px.choropleth(
    df_long,
    locations="Country",
    color="Uncertainty",
    hover_name="Country",
    animation_frame="Month",
    color_continuous_scale="RdYlBu_r",
    range_color=(df_long["Uncertainty"].min(), 1.3),
    projection="natural earth",
    title="IMF World Uncertainty Index by Country"
)

fig.update_layout(
    margin=dict(t=80, b=80),
    annotations=[
        dict(
            text="Source: https://worlduncertaintyindex.com/",
            x=0.5, y=-0.25,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=14)
        )
    ]
)

# Dash app
app = Dash(__name__)
app.title = "IMF Uncertainty Dashboard"

app.layout = html.Div([
    html.H2("IMF World Uncertainty Index - Animated Choropleth"),
    dcc.Graph(figure=fig),
    html.Div("Source: https://worlduncertaintyindex.com/", style={"textAlign": "center", "marginTop": 20})
])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
