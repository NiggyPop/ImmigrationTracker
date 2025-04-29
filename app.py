import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------
# Page Configuration
# ------------------------------
st.set_page_config(
    page_title="Immigration Comparison Dashboard",
    page_icon="🧳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------
# Custom Styling
# ------------------------------
st.markdown(
    """
    <style>
        .main {
            background-color: #f9f9f9;
        }
        .sidebar .sidebar-content {
            background-color: #f0f2f6;
        }
        h1 {
            color: #333333;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Load Data
# ------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("immigration_term_comparison.csv")

df = load_data()

# ------------------------------
# Sidebar Filters
# ------------------------------
with st.sidebar:
    st.header("Filter Data")
    selected_categories = st.multiselect(
        "Select categories to display:",
        options=df["Category"].unique(),
        default=df["Category"].unique()
    )

    selected_years = st.multiselect(
        "Select term years:",
        options=df["Term Year"].unique(),
        default=df["Term Year"].unique()
    )

# ------------------------------
# Filter and Transform Data
# ------------------------------
filtered_df = df[
    df["Category"].isin(selected_categories) & 
    df["Term Year"].isin(selected_years)
]

# Melt data for long-form plotting
long_df = pd.melt(
    filtered_df,
    id_vars=["Term Year", "Category"],
    value_vars=["Donald Trump", "Joe Biden"],
    var_name="President",
    value_name="Count"
)
long_df["Label"] = long_df["Category"] + " - " + long_df["President"]

# Sort by count within each year
long_df.sort_values(["Term Year", "Count"], ascending=[True, False], inplace=True)

# ------------------------------
# Color Palette
# ------------------------------
colors = [
    "#332288", "#117733", "#44AA99", "#88CCEE", "#DDCC77",
    "#CC6677", "#AA4499", "#882255", "#661100", "#999933"
]
unique_labels = long_df["Label"].unique()
color_map = {label: colors[i % len(colors)] for i, label in enumerate(unique_labels)}

# ------------------------------
# Plot
# ------------------------------
fig = px.bar(
    long_df,
    x="Term Year",
    y="Count",
    color="Label",
    color_discrete_map=color_map,
    barmode="group",
    title="Immigration Data Comparison by Presidential Term Year (Sorted by Quantity)"
)

fig.update_layout(
    template="plotly_white",
    font=dict(family="Helvetica", size=14),
    plot_bgcolor="#f9f9f9",
    paper_bgcolor="#f9f9f9",
    xaxis_title="Term Year",
    yaxis_title="Number of People",
    legend_title="Category - President"
)

# ------------------------------
# Display
# ------------------------------
st.title("🧳 Immigration Comparison Dashboard")
st.markdown("Analyze immigration trends across presidential terms by category and year.")

st.plotly_chart(fig, use_container_width=True)
