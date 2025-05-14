import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Load and prepare data
df = pd.read_excel("WUI M Dataset Apr 2025.xlsx", sheet_name="T1")
df_long = df.melt(id_vars=["date"], var_name="Country", value_name="Uncertainty")
df_long["Month"] = df_long["date"].dt.strftime("%Y-%m")
df_long["Month_Label"] = df_long["date"].dt.strftime("%B %Y")

# Create Plotly Express choropleth
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

# Add custom annotations for month labels to each frame
month_labels = df_long.drop_duplicates("Month")[["Month", "Month_Label"]].set_index("Month").to_dict()["Month_Label"]

for frame in fig.frames:
    label = month_labels.get(frame.name)
    frame.layout = go.Layout(
        annotations=[
            dict(
                text=label,
                x=0.5,
                y=0.18,
                xref="paper",
                yref="paper",
                font=dict(size=36, color="black"),
                showarrow=False,
                xanchor="center"
            )
        ]
    )

# Layout cleanup
fig.update_layout(margin=dict(t=80, b=80))

# Initialize Dash app
app = Dash(__name__)
app.title = "IMF Uncertainty Dashboard"

app.layout = html.Div([
    html.H2("IMF World Uncertainty Index - Animated Choropleth"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
