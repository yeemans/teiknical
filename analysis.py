import pandas as pd
import matplotlib.pyplot as plt
import sqlite3  
import streamlit as st
import plotly.express as px

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

    st.title("Part 2: Cell Type Frequencies per Sample")
    st.dataframe(
        initial_analysis_df.drop(columns=["condition", "treatment", "sample_type", "response"]),
        height=500   # for scrolling
    )

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
    st.title("Part 3: Responder vs Nonresponder Population Breakdowns")
    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.box(
            respond_populations_df,
            x="population",
            y="percentage",
            title="Responder Population Breakdown",
            points="outliers"
        )

        fig1.update_xaxes(tickangle=45)

        st.plotly_chart(fig1)

    with col2:
        fig2 = px.box(
            not_respond_populations_df,
            x="population",
            y="percentage",
            title="Nonresponder Population Breakdown",
            points="outliers"
        )

        fig2.update_xaxes(tickangle=45)

        st.plotly_chart(fig2)

    st.markdown("Population breakdowns between responders and nonresponders are very similar." \
    " The largest proportional difference is that nonresponders have 3.78% more B cells")

def data_subset_analysis():
    melanoma_baseline_miraclib_query = """
    SELECT * 
    FROM cells
    WHERE condition = 'melanoma'
    AND treatment = 'miraclib'
    AND time_from_treatment_start = 0
    """

    cursor.execute(melanoma_baseline_miraclib_query)
    melanoma_baseline_miraclib = cursor.fetchall()
    print(len(melanoma_baseline_miraclib))

    grouped_by_project_query = """
    SELECT project, COUNT(*)
    FROM cells
    WHERE condition = 'melanoma'
    AND treatment = 'miraclib'
    AND time_from_treatment_start = 0
    GROUP BY project
    """

    cursor.execute(grouped_by_project_query)
    grouped_by_project = cursor.fetchall()
    print(grouped_by_project)

    grouped_by_responder_query = """
    SELECT response, COUNT(*)
    FROM cells
    WHERE condition = 'melanoma'
    AND treatment = 'miraclib'
    AND time_from_treatment_start = 0
    GROUP BY response
    """
    cursor.execute(grouped_by_responder_query)
    grouped_by_responder = cursor.fetchall()
    print(grouped_by_responder)

    grouped_by_sex_query = """
    SELECT sex, COUNT(*)
    FROM cells
    WHERE condition = 'melanoma'
    AND treatment = 'miraclib'
    AND time_from_treatment_start = 0
    GROUP BY sex
    """
    cursor.execute(grouped_by_sex_query)
    grouped_by_sex = cursor.fetchall()
    print(grouped_by_sex)

"""
Considering Melanoma males, what is the average number of 
B cells for responders at time=0? Use two decimals (XXX.XX).
"""
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

initial_analysis_visualization()

#data_subset_analysis()
#print(melanoma_males())


statistical_analysis_visualization()