import requests # type: ignore # typ#e: ignore
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