#!/usr/bin/env python3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────────────────────
# 1. Load & reshape your data
# ──────────────────────────────────────────────────────────────────────────────
df = pd.read_excel('WUI M Dataset Apr 2025.xlsx', sheet_name='T1')
df_long = df.melt(
    id_vars=['date'],
    var_name='Country',
    value_name='Uncertainty'
)
df_long['Month'] = df_long['date'].dt.strftime('%Y-%m')
months = sorted(df_long['Month'].unique())

# ──────────────────────────────────────────────────────────────────────────────
# 2. Determine color‐scale bounds
# ──────────────────────────────────────────────────────────────────────────────
min_val = df_long['Uncertainty'].min()
max_val = 1.3  # cap to force red at 1.3

# ──────────────────────────────────────────────────────────────────────────────
# 3. Build animated choropleth with Plotly Express
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
# 4. Style the map & colorbar
# ──────────────────────────────────────────────────────────────────────────────
fig.update_geos(showcoastlines=True, coastlinecolor='black')
fig.update_coloraxes(colorbar_title='Uncertainty')

# ──────────────────────────────────────────────────────────────────────────────
# 5. Override animation timings (2 s hold, 1 s transition)
# ──────────────────────────────────────────────────────────────────────────────
fig.layout.updatemenus[0].buttons[0].args[1].update(
    frame=dict(duration=2000, redraw=True),
    transition=dict(duration=1000, easing='cubic-in-out')
)
fig.layout.sliders[0].update(
    transition=dict(duration=1000, easing='cubic-in-out')
)

# ──────────────────────────────────────────────────────────────────────────────
# 6. Add big month label in each frame
# ──────────────────────────────────────────────────────────────────────────────
for frame in fig.frames:
    dt = pd.to_datetime(frame.name)
    frame.layout = {
        'annotations': [dict(
            text=dt.strftime('%B %Y'),
            x=0.5, y=0.15,
            xref='paper', yref='paper',
            xanchor='center', showarrow=False,
            font=dict(size=36)
        )]
    }

# ──────────────────────────────────────────────────────────────────────────────
# 7. Source attribution
# ──────────────────────────────────────────────────────────────────────────────
fig.add_annotation(
    text="Source: https://worlduncertaintyindex.com/",
    x=0.5, y=-0.2,
    xref='paper', yref='paper',
    showarrow=False
)

# ──────────────────────────────────────────────────────────────────────────────
# 8. Force the initial frame to the last month (rebuild approach)
# ──────────────────────────────────────────────────────────────────────────────
last_idx = len(fig.frames) - 1
fig.layout.sliders[0].active = last_idx

fig = go.Figure(
    data=fig.frames[last_idx].data,
    frames=fig.frames,
    layout=fig.layout
)

# ──────────────────────────────────────────────────────────────────────────────
# 9. Add static label for the last frame
# ──────────────────────────────────────────────────────────────────────────────
fig.add_annotation(
    text=pd.to_datetime(months[-1]).strftime('%B %Y'),
    x=0.5, y=0.15,
    xref='paper', yref='paper',
    xanchor='center', showarrow=False,
    font=dict(size=36)
)

# ──────────────────────────────────────────────────────────────────────────────
# 10. Export to HTML without the initial burst
# ──────────────────────────────────────────────────────────────────────────────
fig.write_html(
    "wui_animation.html",
    auto_play=False  # prevents auto‐play on load
)

# ──────────────────────────────────────────────────────────────────────────────
# 11. (Optional) Launch in browser
# ──────────────────────────────────────────────────────────────────────────────
fig.show()
