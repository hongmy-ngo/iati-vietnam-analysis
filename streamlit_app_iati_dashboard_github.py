import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------
# Seitenlayout
# -------------------------------------------------

st.set_page_config(
    page_title="Vietnam Development Aid Dashboard",
    layout="wide"
)

st.title("Vietnam Development Aid Dashboard")

st.markdown("""
Dieses Dashboard analysiert Entwicklungsprojekte in Vietnam auf Basis von IATI-Daten.
Projektbezogene Kennzahlen werden anhand eindeutiger Projekt-IDs berechnet, um Mehrfachzählungen zu vermeiden.
""")

# -------------------------------------------------
# Daten laden
# -------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        r"data/IATI_activities_vietnam.csv" 
    )

    df["year"] = pd.to_datetime(
        df["day_start"],
        errors="coerce"
    ).dt.year

    return df


df = load_data()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

st.sidebar.header("Filter")

organizations = sorted(df["reporting"].dropna().unique())

selected_orgs = st.sidebar.multiselect(
    "Reporting Organization",
    options=organizations,
    default=organizations
)

sectors = sorted(df["sector_group"].dropna().unique())

selected_sectors = st.sidebar.multiselect(
    "Sector",
    options=sectors,
    default=sectors
)

years = sorted(df["year"].dropna().unique())

selected_years = st.sidebar.slider(
    "Year Range",
    int(min(years)),
    int(max(years)),
    (int(min(years)), int(max(years)))
)

# -------------------------------------------------
# Filter anwenden
# -------------------------------------------------

filtered_df = df.copy()

if selected_orgs:
    filtered_df = filtered_df[
        filtered_df["reporting"].isin(selected_orgs)
    ]

filtered_df = filtered_df[
    filtered_df["sector_group"].isin(selected_sectors)
]

filtered_df = filtered_df[
    (filtered_df["year"] >= selected_years[0]) &
    (filtered_df["year"] <= selected_years[1])
]

# -------------------------------------------------
# Eindeutige Projekte erzeugen
# -------------------------------------------------

projects_df = filtered_df.drop_duplicates(subset="slug")

# -------------------------------------------------
# KPIs
# -------------------------------------------------

total_projects = len(projects_df)
total_budget = projects_df["commitment_eur"].sum()
total_spend = projects_df["spend_eur"].sum()

if total_budget > 0:
    utilization = total_spend / total_budget * 100
else:
    utilization = 0

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Projects",
    f"{total_projects:,}"
)

col2.metric(
    "Budget",
    f"€ {total_budget/1_000_000:,.1f} M"
)

col3.metric(
    "bisherige Ausgaben",
    f"€ {total_spend/1_000_000:,.1f} M"
)

col4.metric(
    "Budget Utilization",
    f"{utilization:.1f}%"
)

st.divider()

# -------------------------------------------------
# Top-Sektoren
# -------------------------------------------------

col_left, col_right = st.columns(2)

with col_left:

    sector = (
        filtered_df
        .groupby("sector_group")["commitment_eur"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig_sector = px.bar(
        sector,
        x="sector_group",
        y="commitment_eur",
        title="Top 10 Sectors",
        color_discrete_sequence=["#052691"]
    )

    fig_sector.update_layout(
        xaxis_title="Sector",
        yaxis_title="Committed Budget (€)"
    )

    st.plotly_chart(
        fig_sector,
        use_container_width=True
    )

with col_right:

    status = (
        projects_df["status_code"]
        .value_counts()
        .reset_index()
    )

    status.columns = ["status_code", "count"]

    fig_status = px.pie(
        status,
        names="status_code",
        values="count",
        title="Project Status"
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )

# -------------------------------------------------
# Zeitentwicklung
# -------------------------------------------------

time = (
    projects_df
    .groupby("year")["commitment_eur"]
    .sum()
    .reset_index()
)

fig_time = px.line(
    time,
    x="year",
    y="commitment_eur",
    title="Budget Development Over Time",
    markers=True,
    color_discrete_sequence=["#052691"]
)

fig_time.update_layout(
    xaxis_title="Year",
    yaxis_title="Committed Budget (€)"
)

st.plotly_chart(
    fig_time,
    use_container_width=True
)

# -------------------------------------------------
# Scatterplot
# -------------------------------------------------

fig_scatter = px.scatter(
    projects_df,
    x="commitment_eur",
    y="spend_eur",
    color="status_code",
    hover_data=["title"],
    title="Budget vs Expenditure",
    labels={
        "commitment_eur": "Committed Budget (€)",
        "spend_eur": "Expenditure (€)",
        "status_code": "Status"
    }
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True
)

# -------------------------------------------------
# Datenqualität
# -------------------------------------------------

st.subheader("Data Quality")

missing = (
    df.isna()
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

missing.columns = [
    "Variable",
    "Missing Values"
]

fig_missing = px.bar(
    missing.head(10),
    x="Variable",
    y="Missing Values",
    title="Top 10 Variables with Missing Values"
)

st.plotly_chart(
    fig_missing,
    use_container_width=True
)

# -------------------------------------------------
# Projekttabelle
# -------------------------------------------------

st.subheader("Project Overview")

columns_to_show = [
    "reporting",
    "title",
    "sector_group",
    "commitment_eur",
    "spend_eur",
    "status_code"
]

st.dataframe(
    projects_df[columns_to_show],
    use_container_width=True
)