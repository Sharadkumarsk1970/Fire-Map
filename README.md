# Fire-Map
Visualize and Animate Fire Heatmap 

Interactive Fire Detection Map of India (2022–2024)
This project visualizes high-confidence fire detections across India from 2022 to 2024 using NASA's MODIS Fire Archive data. The outputs include:

An animated heatmap of fire incidents over time.

Clustered markers for days with extreme fire activity.

An interactive line chart showing monthly fire trends.

Files Used
File Name	Description
fire_archive_M-C61_621242_22.csv	MODIS fire data for 2022
fire_archive_M-C61_621247_23.csv	MODIS fire data for 2023
fire_archive_M-C61_621251_24.csv	MODIS fire data for 2024
india_states.geojson	GeoJSON file containing Indian state boundaries
interactive_fire_map.html	Output HTML map with heatmap and clusters
monthly_fire_trend.html	Output HTML of monthly fire count line chart

Workflow Overview
1. Load and Preprocess Fire Data
Combine MODIS fire CSV files for 2022, 2023, and 2024.

Filter out low-confidence detections (retain records with confidence > 80).

Apply geographic filtering to limit the data to India (latitude 6–38, longitude 68–98).

Extract and format dates for use in temporal analysis.

2. Generate Animated Heatmap
Use folium and HeatMapWithTime to create a dynamic, time-series visualization of fire locations.

Intensity is based on the recorded brightness of each fire detection.

3. Add State Boundaries
Load Indian state boundaries from a GeoJSON file and overlay them on the base map for spatial context.

4. Highlight Peak Fire Days
Identify days with more than 1,000 fire detections.

Use clustered markers to highlight intense fire activity on these days.

5. Monthly Trend Line Chart
Group fire detections by month.

Use plotly.express to generate an interactive line chart.

Export the chart to monthly_fire_trend.html.

Output
interactive_fire_map.html
Contains an animated heatmap with state overlays and marker clusters for peak fire days.

monthly_fire_trend.html
Displays an interactive line chart showing monthly fire detection trends from 2022 to 2024.

How to Share the Map
To make the HTML visualizations publicly accessible (for example, on LinkedIn), you need to host them online. Some options include:

GitHub Pages

Netlify

Google Drive (public sharing)

Note: Sharing a local file path like file:///D:/... will not work online.

Requirements
Install the required Python libraries:

bash
Copy
Edit
pip install pandas folium plotly
Optional dependencies (for enhanced functionality):

bash
Copy
Edit
pip install geopandas pyogrio
Credits
Fire data: NASA FIRMS MODIS Collection 6.1

Map rendering: Folium

Interactive plotting: Plotly
