from scrape_cbp_encounters import scrape_cbp_encounters
from immigration_data_builder import build_immigration_data
from immigration_chart_creator import create_chart

def main():
    scrape_cbp_encounters()
    build_immigration_data()
    create_chart()

if __name__ == "__main__":
    main()
