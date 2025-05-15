# IMF World Uncertainty Index Animation

## 📝 Aim & Motivation

Economic uncertainty influences policymaking, investment strategies, and global market behavior. This project visualizes the IMF’s World Uncertainty Index (WUI) as an interactive, animated global map, enabling readers to observe how uncertainty fluctuates across countries and over time.

## 🗄️ Data Source

Data for the World Uncertainty Index (WUI) is provided by the World Uncertainty Index project, developed by IMF researchers and detailed in Ahir, Bloom & Furceri (2018). The index quantifies the frequency of the word “uncertainty” (and related terms) in global and country-specific news sources—primarily the Economist Intelligence Unit country reports and major newspapers—to produce a monthly uncertainty measure for over 180 economies. The dataset spans January 1990 to the present, with updates released monthly. You can download the latest Excel or CSV files at [https://worlduncertaintyindex.com/](https://worlduncertaintyindex.com/). In this project, we use the `T1` sheet, which contains:

* `date` (YYYY-MM-DD) — the first day of each month
* ISO-3166 country codes as column headers
* Uncertainty index values by country for each month

---

## ⚙️ Prerequisites

* Python 3.8+
* `pandas`
* `plotly` (>=5.0)

Install dependencies with:

```bash
pip install pandas plotly
```

---

## 🔧 Installation & Setup

1. Clone or download this repository.
2. Place your IMF WUI Excel file (e.g. `WUI M Dataset Apr 2025.xlsx`) in the project root.
3. Ensure the sheet name (e.g. `T1`) matches in the script.
4. Open the script (`wui_heatmap.py`) and adjust the `max_val` if you want a different upper color bound.

---

## 🚀 Usage

Run the script from your terminal:

```bash
python wui_heatmap.py
```

This will generate:

* `wui_animation.html` — an interactive, self‐contained HTML file.

Open it in any modern browser to view:

* ▶️ **Play** button to animate month‐by‐month.
* ▶️ **Slider** to jump to any month.
* ❌ **No autoplay** on load (preventing the initial burst).

---

## 🛠 Key Customizations

1. **Color Scale Range:**

   ```python
   range_color=(df_long.Uncertainty.min(), 1.3)
   ```

   Caps the top of the scale so red always appears for the highest values.

2. **Animation Timing:**

   ```python
   frame=dict(duration=2000, redraw=True)
   transition=dict(duration=1000, easing='cubic-in-out')
   ```

   Holds each frame for 2s, then smoothly eases over 1s.

3. **Initial Frame:**

   ```python
   # Force the map to load on the last month
   fig.layout.sliders[0].active = len(fig.frames) - 1
   fig = go.Figure(data=fig.frames[-1].data, frames=fig.frames, layout=fig.layout)
   ```

   Ensures the HTML preview starts on the most recent date.

4. **Month Labels:**
   Injects a large month label into each frame’s annotations, replacing old labels to avoid stacking.

   ```python
   for frame in fig.frames:
       frame.layout = {'annotations': [month_label(frame.name)]}
   ```

---

## 💡 Embedding in Your Blog

You can simply iframe the `wui_animation_px.html` file:

```html
<iframe src="/path/to/wui_animation.html" width="100%" height="600"></iframe>
```

Readers will get a fully interactive experience without additional setup.

---

## 📝 License & Attribution

Data source: [WorldUncertaintyIndex.com](https://worlduncertaintyindex.com)
