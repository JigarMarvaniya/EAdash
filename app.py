import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.set_page_config(layout="wide", page_title="Employee Attrition Dashboard")

# -- Load data
@st.cache_data
def load_data():
    df = pd.read_csv("EA.csv")
    return df

df = load_data()

# --- Sidebar Filters ---
st.sidebar.title("Filters")

# Safe defaults for missing columns
def safe_unique(df, col):
    return df[col].unique().tolist() if col in df.columns else []

dept_options = safe_unique(df, 'Department')
jobrole_options = safe_unique(df, 'JobRole')
gender_options = safe_unique(df, 'Gender')
education_options = safe_unique(df, 'Education')
marital_options = safe_unique(df, 'MaritalStatus')
overtime_options = safe_unique(df, 'OverTime')

selected_depts = st.sidebar.multiselect("Department", dept_options, default=dept_options)
selected_roles = st.sidebar.multiselect("Job Role", jobrole_options, default=jobrole_options)
selected_genders = st.sidebar.multiselect("Gender", gender_options, default=gender_options)
selected_education = st.sidebar.multiselect("Education", education_options, default=education_options)
selected_marital = st.sidebar.multiselect("Marital Status", marital_options, default=marital_options)
selected_overtime = st.sidebar.multiselect("OverTime", overtime_options, default=overtime_options)

filtered_df = df.copy()
for col, selected in zip(
    ['Department', 'JobRole', 'Gender', 'Education', 'MaritalStatus', 'OverTime'],
    [selected_depts, selected_roles, selected_genders, selected_education, selected_marital, selected_overtime]
):
    if col in filtered_df.columns and selected:
        filtered_df = filtered_df[filtered_df[col].isin(selected)]

st.title("📊 Employee Attrition Insights Dashboard")
st.write("""
This interactive dashboard helps HR leaders and stakeholders explore employee attrition data, uncover key patterns, and make informed decisions.
All charts are interactive and reflect the filters you select.
""")

# --- Tabs
tabs = st.tabs([
    "Overview", "Attrition Breakdown", "Drivers & KPIs", "Demographics", "Data & Downloads"
])

# -------- Overview Tab --------
with tabs[0]:
    st.header("Attrition Rate Overview")
    st.markdown("**Shows the percentage of employees who have left the organization.**")
    attrition_rate = 100 * filtered_df['Attrition'].str.lower().eq('yes').mean() if 'Attrition' in filtered_df.columns else np.nan
    st.metric("Overall Attrition Rate (%)", f"{attrition_rate:.2f}" if not np.isnan(attrition_rate) else "N/A")

    st.markdown("**Distribution of attrition status in the filtered data.**")
    if 'Attrition' in filtered_df.columns:
        fig = px.pie(filtered_df, names="Attrition", title="Attrition Distribution", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**See how attrition varies by department.**")
    if 'Department' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        ct = pd.crosstab(filtered_df['Department'], filtered_df['Attrition'], normalize='index')
        fig = px.bar(ct, barmode='group', title="Attrition Rate by Department")
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("**Attrition count by gender.**")
    if 'Gender' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        fig = px.histogram(filtered_df, x="Gender", color="Attrition", barmode="group", title="Attrition by Gender")
        st.plotly_chart(fig, use_container_width=True)

# -------- Attrition Breakdown Tab --------
with tabs[1]:
    st.header("Attrition Breakdown by Role, Age, Tenure")
    st.markdown("**Which roles, ages, and tenures see the most attrition?**")
    if 'JobRole' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        fig = px.histogram(filtered_df, x="JobRole", color="Attrition", barmode='group', title="Attrition by Job Role")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Age distribution among employees, split by attrition status.**")
    if 'Age' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        fig = px.histogram(filtered_df, x="Age", color="Attrition", nbins=20, barmode='overlay', title="Age Distribution by Attrition")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Monthly Income differences between employees who stayed or left.**")
    if 'MonthlyIncome' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        fig = px.box(filtered_df, x="Attrition", y="MonthlyIncome", points="all", title="Monthly Income by Attrition")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Tenure at company vs attrition (violin plot shows spread and outliers).**")
    if 'YearsAtCompany' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        fig = px.violin(filtered_df, x="Attrition", y="YearsAtCompany", box=True, points="all", title="Years at Company vs Attrition")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Attrition by marital status.**")
    if 'MaritalStatus' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        fig = px.bar(pd.crosstab(filtered_df['MaritalStatus'], filtered_df['Attrition'], normalize='index'), barmode='group', title="Attrition by Marital Status")
        st.plotly_chart(fig, use_container_width=True)

# -------- Drivers & KPIs Tab --------
with tabs[2]:
    st.header("Drivers and Predictors of Attrition")
    st.markdown("**Does working overtime affect attrition?**")
    if 'OverTime' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        fig = px.bar(pd.crosstab(filtered_df['OverTime'], filtered_df['Attrition'], normalize='index'), barmode='group', title="Attrition by Overtime")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Job Satisfaction levels by attrition.**")
    if 'JobSatisfaction' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        fig = px.box(filtered_df, x="Attrition", y="JobSatisfaction", points="all", title="Job Satisfaction by Attrition")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Work-Life Balance scores by attrition.**")
    if 'WorkLifeBalance' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        fig = px.box(filtered_df, x="Attrition", y="WorkLifeBalance", points="all", title="Work-Life Balance by Attrition")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Years Since Last Promotion: Do those who leave feel stuck?**")
    if 'YearsSinceLastPromotion' in filtered_df.columns and 'Attrition' in filtered_df.columns:
        fig = px.box(filtered_df, x="Attrition", y="YearsSinceLastPromotion", points="all", title="Years Since Last Promotion by Attrition")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**See correlation between all numeric features.**")
    num_cols = filtered_df.select_dtypes(include=np.number).columns
    if len(num_cols) > 1:
        corr = filtered_df[num_cols].corr()
        fig, ax = plt.subplots(figsize=(8,5))
        sns.heatmap(corr, cmap="coolwarm", annot=False, ax=ax)
        st.pyplot(fig)

# -------- Demographics Tab --------
with tabs[3]:
    st.header("Demographic Insights")
    st.markdown("**Breakdown of education levels among employees.**")
    if 'Education' in filtered_df.columns:
        fig = px.histogram(filtered_df, x="Education", color="Attrition" if 'Attrition' in filtered_df.columns else None, barmode='group', title="Education Levels")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Distribution of employees by gender and age.**")
    if 'Gender' in filtered_df.columns and 'Age' in filtered_df.columns:
        fig = px.histogram(filtered_df, x="Age", color="Gender", barmode="overlay", nbins=20, title="Age Distribution by Gender")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Hierarchical breakdown: Department > Job Role > Attrition.**")
    if all(col in filtered_df.columns for col in ['Department', 'JobRole', 'Attrition']):
        fig = px.sunburst(filtered_df, path=['Department', 'JobRole', 'Attrition'], title="Organization Hierarchy Sunburst")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**See a sample of the filtered data.**")
    st.dataframe(filtered_df.head(10))

# -------- Data & Downloads Tab --------
with tabs[4]:
    st.header("Data and Downloads")
    st.markdown("**Download your current filtered data as CSV.**")
    csv = filtered_df.to_csv(index=False).encode()
    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_EA.csv",
        mime="text/csv"
    )

    st.markdown("**Summary statistics for numeric columns.**")
    st.dataframe(filtered_df.describe(include='all'))

    st.markdown("**Create your own pivot table for analysis.**")
    cols = filtered_df.columns.tolist()
    row = st.selectbox("Row", cols, key="row")
    col = st.selectbox("Column", cols, key="col")
    agg = st.selectbox("Aggregation", ["count", "mean", "sum", "min", "max"], key="agg")
    if row and col:
        try:
            pt = pd.pivot_table(filtered_df, index=row, columns=col, aggfunc=agg)
            st.dataframe(pt)
        except Exception as e:
            st.warning(f"Pivot error: {e}")

st.caption("Dashboard built with Streamlit | For HR Insights | Version 1.0")
