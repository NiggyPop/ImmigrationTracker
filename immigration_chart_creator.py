import pandas as pd
import plotly.graph_objects as go

def create_chart():
    tol_colors = [
        "#332288", "#117733", "#44AA99", "#88CCEE",
        "#DDCC77", "#CC6677", "#AA4499", "#882255",
        "#661100", "#999933"
    ]

    df = pd.read_csv("immigration_term_comparison.csv")
    fig = go.Figure()
    categories = df['Category'].unique()
    color_map = {category: tol_colors[i % len(tol_colors)] for i, category in enumerate(categories)}

    for category in categories:
        df_cat = df[df['Category'] == category]
        fig.add_trace(go.Bar(
            x=df_cat["Term Year"],
            y=df_cat["Trump"],
            name=f"{category} - Donald Trump",
            marker_color=color_map[category],
            offsetgroup=category,
            legendgroup=category
        ))
        fig.add_trace(go.Bar(
            x=df_cat["Term Year"],
            y=df_cat["Biden"],
            name=f"{category} - Joe Biden",
            marker_color=color_map[category],
            offsetgroup=category,
            base=0,
            legendgroup=category,
            opacity=0.6
        ))

    fig.update_layout(
        title="Immigration Data Comparison by Presidential Term Year",
        xaxis_title="Term Year",
        yaxis_title="Number of People",
        barmode='group',
        template='plotly_white',
        legend_title="Category"
    )

    fig.write_html("immigration_term_comparison.html")
    print("Saved immigration_term_comparison.html")
