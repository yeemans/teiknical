from pipeline import initial_analysis, statistical_analysis, data_subset_analysis
import streamlit as st
import plotly.express as px

def initial_analysis_dashboard():
    initial_analysis_df = initial_analysis()
    st.title("Part 2: Cell Type Frequencies per Sample")
    st.dataframe(
        initial_analysis_df.drop(columns=["condition", "treatment", "sample_type", "response"]),
        height=500   # for scrolling
    )

def statistical_analysis_dashboard():
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

def data_subset_analysis_dashboard():
    melanoma_df, project_df, responder_df, sex_df = data_subset_analysis()
    st.title("Part 4: Melanoma Subset Analysis")
    st.markdown("Table of PBMC melanoma samples at baseline treated with Miraclib")
    st.dataframe(
        melanoma_df,
        height=500   # for scrolling
    )

    st.markdown("Breakdown by project")
    fig = px.bar(
        project_df,
        x="project",
        y="count",
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Breakdown by response")
    fig = px.bar(
        responder_df,
        x="response",
        y="count",
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("Breakdown by sex")
    fig = px.bar(
        sex_df,
        x="sex",
        y="count",
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)
    

initial_analysis_dashboard()
statistical_analysis_dashboard()
data_subset_analysis_dashboard()