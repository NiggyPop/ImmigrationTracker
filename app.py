
import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("immigration_term_comparison.csv")

# Sidebar filters
st.sidebar.header("Filter Data")
selected_categories = st.sidebar.multiselect(
    "Select categories to display:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

selected_years = st.sidebar.multiselect(
    "Select term years:",
    options=df["Term Year"].unique(),
    default=df["Term Year"].unique()
)

# Filter data
filtered_df = df[
    df["Category"].isin(selected_categories) & 
    df["Term Year"].isin(selected_years)
]

# Melt the data for easier sorting and plotting
long_df = pd.melt(
    filtered_df,
    id_vars=["Term Year", "Category"],
    value_vars=["Donald Trump", "Joe Biden"],
    var_name="President",
    value_name="Count"
)

# Add a combined label for display
long_df["Label"] = long_df["Category"] + " - " + long_df["President"]

# Sort within each Term Year by Count
long_df.sort_values(["Term Year", "Count"], ascending=[True, False], inplace=True)

# Color mapping
colors = [
    "#332288", "#117733", "#44AA99", "#88CCEE", "#DDCC77",
    "#CC6677", "#AA4499", "#882255", "#661100", "#999933"
]
unique_labels = long_df["Label"].unique()
color_map = {label: colors[i % len(colors)] for i, label in enumerate(unique_labels)}

# Plot using Plotly Express
fig = px.bar(
    long_df,
    x="Term Year",
    y="Count",
    color="Label",
    color_discrete_map=color_map,
    barmode="group",
    title="Immigration Data Comparison by Presidential Term Year (Sorted by Quantity)",
)

fig.update_layout(
    xaxis_title="Term Year",
    yaxis_title="Number of People",
    legend_title="Category - President",
    template="plotly_white"
)

# Display
st.title("Immigration Comparison Dashboard")
st.plotly_chart(fig, use_container_width=True)
