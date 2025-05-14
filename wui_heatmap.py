import pandas as pd
import plotly.graph_objects as go

# Sample data frame `df` with columns: "country_code", "value", "date"
# Replace this with your actual data
df = pd.read_excel('WUI M Dataset Apr 2025.xlsx', sheet_name='T1')

# Prepare data for animation
df_long = df.melt(id_vars=['date'], var_name='Country', value_name='Uncertainty')
df_long['Month'] = df_long['date'].dt.strftime('%Y-%m')

# Set the maximum value of the color scale to 1.3 (as per your request)
min_value = df_long['Uncertainty'].min()
max_value = 1.3  # Explicitly setting the max value to 1.3 to ensure it's in red

# Create traces for the map
trace = go.Choropleth(
    locations=df_long['Country'],
    z=df_long['Uncertainty'],
    text=df_long['Country'],
    hoverinfo="location+z+text",
    colorscale="RdYlBu_r",
    colorbar=dict(title="Uncertainty"),
    zmin=min_value,
    zmax=max_value
)

# Create frames for the animation
frames = [go.Frame(
    data=[go.Choropleth(
        locations=df_long[df_long['Month'] == month]['Country'],
        z=df_long[df_long['Month'] == month]['Uncertainty'],
        text=df_long[df_long['Month'] == month]['Country'],
        hoverinfo="location+z+text",
        colorscale="RdYlBu_r",
        colorbar=dict(title="Uncertainty"),
        zmin=min_value,
        zmax=max_value
    )],
    name=month
) for month in df_long['Month'].unique()]

# Define layout and animation settings
layout = go.Layout(
    title="IMF World Uncertainty Index by Country",
    geo=dict(showcoastlines=True, coastlinecolor="Black", projection_type="natural earth"),
    updatemenus=[{
        'buttons': [
            {
                'args': [None, {'frame': {'duration': 2000, 'redraw': True}, 'fromcurrent': True}],  # Frame duration set to 2000ms
                'label': 'Play',
                'method': 'animate',
            },
        ],
        'direction': 'left',
        'pad': {'r': 10, 't': 87},
        'showactive': False,
        'type': 'buttons',
        'x': 0.1,
        'xanchor': 'right',
        'y': 0,
        'yanchor': 'bottom',
    }],
    sliders=[{
        'steps': [{
            'args': [
                [str(month)],
                {'frame': {'duration': 2000, 'redraw': True},  # 2000ms per frame
                 'mode': 'immediate',
                 'transition': {'duration': 2000, 'easing': 'ease-in-out'}},  # Smooth transition between frames
            ],
            'label': f'{month}',
            'method': 'animate',
        } for month in df_long['Month'].unique()]
    }],
    annotations=[dict(
        text="Source: https://worlduncertaintyindex.com/",  # Source URL text
        x=0.5, y=-0.6,  # Position below the slider (adjust y to move it further down)
        xref="paper", yref="paper",  # Reference to paper coordinates
        font=dict(size=14, color="black"),
        showarrow=False
    )]
)

# Create the figure with data, layout, and frames
fig = go.Figure(
    data=[trace],
    layout=layout,
    frames=frames
)

# Add dynamic month labels to each frame
for frame in fig.frames:
    date_val = pd.to_datetime(frame.name)  # Assuming frame.name is date-like
    label = date_val.strftime("%B %Y")
    frame.layout.annotations = [dict(
        text=label, x=0.5, y=0.18, xref="paper", yref="paper",  # Position in the lower half (y=0.1)
        xanchor="center", font=dict(size=36, color="black"), showarrow=False
    )]

# Save the animation as HTML (for viewing in the browser with transitions)
fig.write_html("IMF_Uncertainty_Index_Animation_Interactive_with_Consistent_Colors_and_Source.html")

# Show the figure interactively (this will make the transition work with smooth transitions when opened in the browser)
fig.show()
