import pandas as pd
import folium
from folium.plugins import HeatMapWithTime, MarkerCluster
import plotly.express as px
from datetime import datetime
import json

# File paths
file_2022 = "fire_archive_M-C61_621242_22.csv"
file_2023 = "fire_archive_M-C61_621247_23.csv"
file_2024 = "fire_archive_M-C61_621251_24.csv"
geojson_path = "india_states.geojson"

#  Load and combine data
df = pd.concat([
    pd.read_csv(file_2022),
    pd.read_csv(file_2023),
    pd.read_csv(file_2024)
], ignore_index=True)

#  Preprocessing
df['acq_date'] = pd.to_datetime(df['acq_date'], errors='coerce')
df = df[pd.to_numeric(df['confidence'], errors='coerce') > 80]
df = df[df['latitude'].between(6, 38) & df['longitude'].between(68, 98)]

# Format date label for better readability (e.g. "01 Jan 2023")
df['date_label'] = df['acq_date'].dt.strftime('%d %b %Y')
df['date'] = df['acq_date'].dt.strftime('%Y-%m-%d')

# Prepare heatmap data
dates = sorted(df['date'].dropna().unique())
date_labels = df.drop_duplicates(subset='date').set_index('date').loc[dates]['date_label'].tolist()

heat_data = []
for day in dates:
    daily = df[df['date'] == day]
    heat_data.append([[row['latitude'], row['longitude'], row['brightness']] for _, row in daily.iterrows()])

# Create map
m = folium.Map(location=[22.5, 80], zoom_start=5, tiles="cartodb positron")

# 🧾 Add State Boundaries
with open(geojson_path, "r", encoding="utf-8") as f:
    india_states = json.load(f)

folium.GeoJson(
    india_states,
    name="State Boundaries",
    style_function=lambda x: {
        'color': 'gray',
        'weight': 1.5,
        'fillOpacity': 0.1
    }
).add_to(m)

# Add Animated Heatmap with formatted date labels
HeatMapWithTime(
    data=heat_data,
    index=date_labels,
    auto_play=True,
    radius=2,
    scale_radius=True,
    max_opacity=0.6,
    gradient={0.2: 'blue', 0.4: 'lime', 0.6: 'orange', 1: 'red'},
    display_index=True
).add_to(m)

#  Add MarkerCluster for peak fire days
peak_days = df['date'].value_counts()
peak_days = peak_days[peak_days > 1000].index.tolist()

cluster = MarkerCluster(name="Peak Day Clusters").add_to(m)
for day in peak_days:
    daily = df[df['date'] == day]
    for _, row in daily.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3,
            color='crimson',
            fill=True,
            fill_opacity=0.7,
            popup=folium.Popup(f"""
                <b>Date:</b> {row['acq_date']}<br>
                <b>Brightness:</b> {row['brightness']}<br>
                <b>Confidence:</b> {row['confidence']}
            """, max_width=300),
        ).add_to(cluster)

# Monthly trend chart
df['month'] = df['acq_date'].dt.to_period('M')
monthly = df.groupby('month').size().reset_index(name='fire_count')
monthly['month'] = monthly['month'].dt.to_timestamp()

fig = px.line(monthly,
              x='month',
              y='fire_count',
              title='Monthly High-Confidence Fire Detections (2022–2024)',
              markers=True,
              labels={'month': 'Month', 'fire_count': 'Number of Fires'},
              line_shape='spline')
fig.update_layout(template='plotly_dark', hovermode="x unified")
fig.write_html("monthly_fire_trend.html")

# Save map
m.save("interactive_fire_map.html")

print("✅ Saved: interactive_fire_map.html")
print("✅ Saved: monthly_fire_trend.html")
