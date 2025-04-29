import requests
import pandas as pd
from bs4 import BeautifulSoup

# Step 1: Fetch the CBP Southwest Land Border Encounters page
url = "https://www.cbp.gov/newsroom/stats/southwest-land-border-encounters"
response = requests.get(url)
soup = BeautifulSoup(response.content, "lxml")

# Step 2: Find the right table
# NOTE: CBP sometimes updates their webpage format! Always check HTML structure
# Look for tables or CSV download links

tables = soup.find_all('table')

if not tables:
    raise Exception("No tables found. CBP might have changed their page structure.")

# Step 3: Assume the first table contains total encounters
# (This may need to be adjusted based on page layout!)

df_list = pd.read_html(str(tables[0]))
encounter_df = df_list[0]

# Step 4: Basic cleaning (depends on how the table is structured)
print(encounter_df.head())

# (Optional) Sum up monthly numbers if necessary
# For now assume annual totals are available or add monthly columns

# Step 5: Save the data
encounter_df.to_csv("cbp_encounters_scraped.csv", index=False)

print("\nScraped CBP Encounter Data Saved!")