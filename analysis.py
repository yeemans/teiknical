import pandas as pd
import copy

def initial_analysis():
    df = pd.read_csv("cell-count.csv")

    output_rows = []
    cell_types = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]

    for _, row in df.iterrows():
        for cell_type in cell_types:

            output_row = {
                "sample": "",
                "total_count": 0,
                "population": "",
                "count": 0,
                "percentage": 0.0
            }

            output_row["sample"] = row["sample"]

            total_count = 0
            for ct in cell_types:
                total_count += row[ct]

            output_row["total_count"] = total_count
            output_row["population"] = cell_type
            output_row["count"] = row[cell_type]
            output_row["percentage"] = output_row["count"] / total_count

            output_rows.append(output_row)

    output_df = pd.DataFrame(output_rows)
    print(output_df)

initial_analysis()