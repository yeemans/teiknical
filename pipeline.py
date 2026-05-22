import pandas as pd
import matplotlib.pyplot as plt
import sqlite3  
import subprocess
import seaborn as sns


CELL_TYPES = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
conn = sqlite3.connect("cells.db")
cursor = conn.cursor()

def initial_analysis():
    df = pd.read_csv("cell-count.csv")

    output_rows = []

    for _, row in df.iterrows():
        for cell_type in CELL_TYPES:

            output_row = {
                "sample": "",
                "total_count": 0,
                "population": "",
                "count": 0,
                "percentage": 0.0
            }

            output_row["sample"] = row["sample"]

            total_count = 0
            for ct in CELL_TYPES:
                total_count += row[ct]

            output_row["total_count"] = total_count
            output_row["population"] = cell_type
            output_row["count"] = row[cell_type]
            output_row["percentage"] = output_row["count"] / total_count * 100

            # to be used in part 3
            output_row["condition"] = row["condition"]
            output_row["treatment"] = row["treatment"]
            output_row["sample_type"] = row["sample_type"]
            output_row["response"] = row["response"]

            output_rows.append(output_row)

    output_df = pd.DataFrame(output_rows)
    print(output_df)
    return output_df

def initial_analysis_visualization():
    initial_analysis_df = initial_analysis()
    export_df = initial_analysis_df.head().drop(columns=["condition", "treatment", "sample_type", "response"])
    export_df.to_html("Cell_Type_Frequencies_per_Sample.html")
    subprocess.call(
    'wkhtmltoimage -f png --width 0 Cell_Type_Frequencies_per_Sample.html Cell_Type_Frequencies_per_Sample_Part2.png', shell=True)

def statistical_analysis():
    # only include pbmc samples
    df = initial_analysis()
    pbmc_df = df[(df["sample_type"] == "PBMC") & (df["condition"] == "melanoma") & (df["treatment"] == "miraclib")]


    # each entry in these lists is a dictionary
    # each entry contains a cell type, and its relative frequency in a row of data
    respond_populations = []
    not_respond_populations = []

    for _, row in pbmc_df.iterrows():
        output_row = {"population": "", "percentage": 0.0}
        output_row["population"] = row["population"]
        output_row["percentage"] = row["percentage"]

        if row["response"] == "yes":
            respond_populations.append(output_row)
        else:
            not_respond_populations.append(output_row)

    respond_populations_df = pd.DataFrame(respond_populations)
    not_respond_populations_df = pd.DataFrame(not_respond_populations)
    return [respond_populations_df, not_respond_populations_df]
    
def statistical_analysis_visualization():
    respond_populations_df, not_respond_populations_df = statistical_analysis()
    # save an image of the 2 boxplots
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    sns.boxplot(data=respond_populations_df, x='population', y='percentage', ax=axes[0])
    axes[0].set_title('Responder Population Breakdowns')

    # Plot second dataframe on the second axis
    sns.boxplot(data=not_respond_populations_df, x='population', y='percentage', ax=axes[1])
    axes[1].set_title('Nonresponder Population Breakdowns')

    plt.tight_layout()
    plt.savefig("Responder_vs_Nonresponder_Population_Breakdowns_Part3")

def data_subset_analysis():
    melanoma_baseline_miraclib_query = """
    SELECT * 
    FROM cells
    WHERE condition = 'melanoma'
    AND treatment = 'miraclib'
    AND sample_type = 'PBMC'
    AND time_from_treatment_start = 0
    """

    melanoma_baseline_miraclib_df = pd.read_sql_query(melanoma_baseline_miraclib_query, conn)


    grouped_by_project_query = """
    SELECT project, COUNT(*) as count
    FROM cells
    WHERE condition = 'melanoma'
    AND treatment = 'miraclib'
    AND sample_type = 'PBMC'
    AND time_from_treatment_start = 0
    GROUP BY project
    """

    grouped_by_project_df = pd.read_sql_query(grouped_by_project_query, conn)


    grouped_by_responder_query = """
    SELECT response, COUNT(*) as count
    FROM cells
    WHERE condition = 'melanoma'
    AND treatment = 'miraclib'
    AND sample_type = 'PBMC'
    AND time_from_treatment_start = 0
    GROUP BY response
    """
    grouped_by_responder_df = pd.read_sql_query(grouped_by_responder_query, conn)

    grouped_by_sex_query = """
    SELECT sex, COUNT(*) as count
    FROM cells
    WHERE condition = 'melanoma'
    AND treatment = 'miraclib'
    AND sample_type = 'PBMC'
    AND time_from_treatment_start = 0
    GROUP BY sex
    """
    grouped_by_sex_df = pd.read_sql_query(grouped_by_sex_query, conn)

    return [melanoma_baseline_miraclib_df, grouped_by_project_df, grouped_by_responder_df,
            grouped_by_sex_df]

def data_subset_analysis_visualization():
    melanoma_df, project_df, responder_df, sex_df = data_subset_analysis()
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))

    # save an image of the table for melanoma
    melanoma_head_df = melanoma_df.head()
    melanoma_head_df.to_html("Melanoma_Baseline_Table.html")
    subprocess.call(
    'wkhtmltoimage -f png --width 0 Melanoma_Baseline_Table.html Melanoma_Baseline_Table_Part4.1.png', shell=True)

    # save an image of the breakdown by project
    plt.clf() # reset settings, so no subplots
    sns.barplot(project_df, x="project", y="count")
    plt.title("Breakdown By Project")
    plt.savefig("Breakdown_By_Project_Part4.21.png")

    plt.clf()
    sns.barplot(responder_df, x="response", y="count")
    plt.title("Breakdown By Response")
    plt.savefig("Breakdown_By_Response_Part4.22.png")

    plt.clf()
    sns.barplot(sex_df, x="sex", y="count")
    plt.title("Breakdown By Sex")
    plt.savefig("Breakdown_By_Sex_Part4.23.png")


def melanoma_males():
    query = """
    SELECT AVG(b_cell)
    FROM cells
    WHERE condition = 'melanoma'
    AND time_from_treatment_start = 0
    AND sex = 'M'
    AND response = 'yes'
    """

    cursor.execute(query)
    answer = cursor.fetchone()[0]
    return answer

print(melanoma_males())
initial_analysis_visualization()
statistical_analysis_visualization()
data_subset_analysis_visualization()