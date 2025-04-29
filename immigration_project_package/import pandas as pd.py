import pandas as pd
import plotly.graph_objects as go

# Define Paul Tol's qualitative color palette
tol_colors = [
    "#332288",  # dark blue
    "#117733",  # dark green
    "#44AA99",  # teal
    "#88CCEE",  # light blue
    "#DDCC77",  # sand
    "#CC6677",  # rose
    "#AA4499",  # purple
    "#882255",  # wine
    "#661100",  # brown
    "#999933",  # olive
]

# Load your data
df = pd.read_csv("immigration_term_comparison.csv")

# Create the figure
fig = go.Figure()

# Get unique categories
categories = df['Category'].unique()

# Assign colors to categories
color_map = {category: tol_colors[i % len(tol_colors)] for i, category in enumerate(categories)}

# Add bars for each category
for category in categories:
    df_cat = df[df['Category'] == category]
    fig.add_trace(go.Bar(
        x=df_cat["Term Year"],
        y=df_cat["Previous Term"],
        name=f"{category} - Previous Term",
        marker_color=color_map[category],
        offsetgroup=category,
        legendgroup=category
    ))
    fig.add_trace(go.Bar(
        x=df_cat["Term Year"],
        y=df_cat["Current Term"],
        name=f"{category} - Current Term",
        marker_color=color_map[category],
        offsetgroup=category,
        base=0,
        legendgroup=category,
        opacity=0.6  # Slightly transparent to distinguish from previous term
    ))

# Update layout
fig.update_layout(
    title="Immigration Data Comparison by Presidential Term Year",
    xaxis_title="Term Year",
    yaxis_title="Number of People",
    barmode='group',
    template='plotly_white',
    legend_title="Category"
)

# Save the figure
fig.write_html("immigration_term_comparison.html")