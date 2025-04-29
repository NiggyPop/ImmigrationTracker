import pandas as pd
import plotly.graph_objects as go

# Step 1: Create a dataset with all categories (values are placeholders for now)
data = {
    "Year": ["2019", "2020", "2021", "2022", "2023", "2024"],
    "Encounters": [1013539, 450000, 600000, 1800000, 2400000, 2200000],
    "TPS Issued": [30000, 45000, 70000, 125000, 200000, 250000],
    "Visas Issued": [9204490, 4253736, 3077152, 7308568, 10901303, 11500000],
    "Citizens Added": [843593, 625000, 814000, 967400, 878500, 900000],
    "Asylum Requested": [60000, 75000, 82000, 120000, 150000, 180000],
    "Turnarounds": [200000, 100000, 150000, 250000, 300000, 320000],
    "Deportation Orders": [250000, 180000, 200000, 310000, 330000, 350000],
    "Expedited Removals": [150000, 120000, 130000, 290000, 300000, 310000],
    "Prisoners (ICE Detained)": [50000, 30000, 40000, 55000, 60000, 58000]
}

df = pd.DataFrame(data)

# Step 2: Combine deportation-related categories
df["Total Deportations"] = (
    df["Turnarounds"] +
    df["Deportation Orders"] +
    df["Expedited Removals"]
)

# Step 3: Save raw data to CSV
df.to_csv("immigration_data_expanded.csv", index=False)

# Step 4: Create stacked bar chart
fig = go.Figure()

categories_to_plot = [
    "Encounters",
    "TPS Issued",
    "Visas Issued",
    "Citizens Added",
    "Asylum Requested",
    "Total Deportations",
    "Prisoners (ICE Detained)"
]

colors = [
    "royalblue", "darkcyan", "gold", "forestgreen", "purple", "firebrick", "grey"
]

for cat, color in zip(categories_to_plot, colors):
    fig.add_trace(go.Bar(
        x=df["Year"],
        y=df[cat],
        name=cat,
        marker_color=color
    ))

# Step 5: Final formatting
fig.update_layout(
    barmode='stack',
    title="U.S. Immigration Data (2019–2024)",
    xaxis_title="Year",
    yaxis_title="Number of People",
    legend_title="Category",
    template="plotly_white"
)

# Step 6: Save and show
fig.write_html("immigration_data_expanded.html")
fig.show()
