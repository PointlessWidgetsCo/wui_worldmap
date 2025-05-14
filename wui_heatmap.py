#!/usr/bin/env python3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────────────────────
# 1. Load & reshape your data
# ──────────────────────────────────────────────────────────────────────────────
df = pd.read_excel('WUI M Dataset Apr 2025.xlsx', sheet_name='T1')
df_long = df.melt(id_vars=['date'], var_name='Country', value_name='Uncertainty')
df_long['Month'] = df_long['date'].dt.strftime('%Y-%m')
months = sorted(df_long['Month'].unique())

# ──────────────────────────────────────────────────────────────────────────────
# 2. Define your color scale bounds
# ──────────────────────────────────────────────────────────────────────────────
min_val = df_long['Uncertainty'].min()
max_val = 1.3  # cap so that top values go red

# ──────────────────────────────────────────────────────────────────────────────
# 3. Build the animated choropleth with Plotly Express
# ──────────────────────────────────────────────────────────────────────────────
fig = px.choropleth(
    df_long,
    locations='Country',
    color='Uncertainty',
    hover_name='Country',
    animation_frame='Month',
    projection='natural earth',
    color_continuous_scale='RdYlBu_r',
    range_color=(min_val, max_val),
    title='IMF World Uncertainty Index by Country'
)

# ──────────────────────────────────────────────────────────────────────────────
# 4. Tweak map & colorbar styling
# ──────────────────────────────────────────────────────────────────────────────
fig.update_geos(showcoastlines=True, coastlinecolor='black')
fig.update_coloraxes(colorbar_title='Uncertainty')

# ──────────────────────────────────────────────────────────────────────────────
# 5. Override Play-button & slider timing
# ──────────────────────────────────────────────────────────────────────────────
fig.layout.updatemenus[0].buttons[0].args[1].update(
    frame=dict(duration=2000, redraw=True),
    transition=dict(duration=1000, easing='cubic-in-out')
)
fig.layout.sliders[0].update(
    transition=dict(duration=1000, easing='cubic-in-out')
)

# ──────────────────────────────────────────────────────────────────────────────
# 6. Inject only the month label into each frame (no source)
# ──────────────────────────────────────────────────────────────────────────────
for frame in fig.frames:
    date_dt = pd.to_datetime(frame.name)
    month_annot = dict(
        text=date_dt.strftime('%B %Y'),
        x=0.5, y=0.15, xref='paper', yref='paper',
        xanchor='center', showarrow=False,
        font=dict(size=36, color='black')
    )
    frame.layout = {'annotations': [month_annot]}

# ──────────────────────────────────────────────────────────────────────────────
# 7. Force initial view → last frame using the “rebuild” trick
# ──────────────────────────────────────────────────────────────────────────────
last_idx = len(fig.frames) - 1
fig.layout.sliders[0].active = last_idx  # moves slider to final month

initial_layout = fig.layout
initial_layout.annotations = fig.frames[last_idx].layout.annotations

fig = go.Figure(
    data=fig.frames[last_idx].data,
    frames=fig.frames,
    layout=initial_layout
)

# ──────────────────────────────────────────────────────────────────────────────
# 8. Export to HTML without the sudden “burst”
# ──────────────────────────────────────────────────────────────────────────────
fig.write_html(
    "wui_animation.html",
    auto_play=False  # disables autoplay on load
)

# ──────────────────────────────────────────────────────────────────────────────
# 9. (Optional) preview in the browser
# ──────────────────────────────────────────────────────────────────────────────
fig.show()
