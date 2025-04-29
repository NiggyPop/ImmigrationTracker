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