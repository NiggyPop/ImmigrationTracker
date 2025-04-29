# Rebuilding everything after environment reset

import zipfile
import os

# Redefine the project files contents
scrape_cbp_encounters_py = """
import requests
import pandas as pd
from bs4 import BeautifulSoup

def scrape_cbp_encounters():
    url = "https://www.cbp.gov/newsroom/stats/southwest-land-border-encounters"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")

    tables = soup.find_all('table')

    if not tables:
        raise Exception("No tables found. CBP might have changed their page structure.")

    df_list = pd.read_html(str(tables[0]))
    encounter_df = df_list[0]

    encounter_df.to_csv("cbp_encounters_scraped.csv", index=False)
    print("Saved cbp_encounters_scraped.csv")
"""

immigration_data_builder_py = """
import pandas as pd

def build_immigration_data():
    categories = [
        "Encounters", "TPS Issued", "Visas Issued", "Citizens Added",
        "Asylum Requested", "Total Deportations", "Prisoners"
    ]
    term_years = ["Year 1", "Year 2", "Year 3", "Year 4"]
    category_values = {
        "Encounters":         ([850000, 950000, 1013539, 450000], [600000, 1800000, 2400000, 2200000]),
        "TPS Issued":         ([20000, 25000, 30000, 45000], [70000, 125000, 200000, 250000]),
        "Visas Issued":       ([9000000, 9100000, 9204490, 4253736], [3077152, 7308568, 10901303, 11500000]),
        "Citizens Added":     ([707265, 760000, 843593, 625000], [814000, 967400, 878500, 900000]),
        "Asylum Requested":   ([55000, 60000, 60000, 75000], [82000, 120000, 150000, 180000]),
        "Total Deportations": ([500000, 520000, 600000, 450000], [480000, 850000, 930000, 980000]),
        "Prisoners":          ([15000, 20000, 50000, 30000], [40000, 55000, 60000, 58000]),
    }

    records = []
    for cat in categories:
        prev_vals, curr_vals = category_values[cat]
        for i, year in enumerate(term_years):
            records.append({
                "Term Year": year,
                "Category": cat,
                "Previous Term": prev_vals[i],
                "Current Term": curr_vals[i]
            })

    df_full = pd.DataFrame(records)
    df_full.to_csv("immigration_term_comparison.csv", index=False)
    print("Saved immigration_term_comparison.csv")
"""

immigration_chart_creator_py = """
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
"""

main_py = """
from scrape_cbp_encounters import scrape_cbp_encounters
from immigration_data_builder import build_immigration_data
from immigration_chart_creator import create_chart

def main():
    scrape_cbp_encounters()
    build_immigration_data()
    create_chart()

if __name__ == "__main__":
    main()
"""

requirements_txt = """
requests
pandas
beautifulsoup4
lxml
plotly
"""

# Write files to disk
project_files = {
    '/mnt/data/scrape_cbp_encounters.py': scrape_cbp_encounters_py,
    '/mnt/data/immigration_data_builder.py': immigration_data_builder_py,
    '/mnt/data/immigration_chart_creator.py': immigration_chart_creator_py,
    '/mnt/data/main.py': main_py,
    '/mnt/data/requirements.txt': requirements_txt
}

for path, content in project_files.items():
    with open(path, 'w') as f:
        f.write(content.strip())

# Zip all project files
zip_path = "/mnt/data/immigration_project_package.zip"
with zipfile.ZipFile(zip_path, 'w') as zipf:
    for file_path in project_files.keys():
        zipf.write(file_path, arcname=os.path.basename(file_path))

zip_path  # Output final ZIP path
