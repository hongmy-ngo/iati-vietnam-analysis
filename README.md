# Vietnam Development Aid Dashboard

A project from my Data Analyst training. I loaded, cleaned and visualized public [IATI data](https://countrydata.iatistandard.org/data/countries/VN/) on development projects in Vietnam — built as two interactive dashboards, one with Dash and one with Streamlit.

**Tools:** Python, pandas, Plotly, Dash, Streamlit

---

## What the dashboard shows

- Number of projects, total budget and expenditure as KPIs
- Top 10 sectors by budget
- Project status (active, completed, planned)
- Budget development over time
- Budget vs. actual expenditure
- Missing values in the dataset (data quality)

---

## Data

Data comes from [countrydata.iatistandard.org](https://countrydata.iatistandard.org/data/countries/VN/) and is not included in this repository. To download:

1. Go to https://countrydata.iatistandard.org/data/countries/VN/
2. Download `IATI activities in Viet Nam` as CSV
3. Save the file as `data/IATI_activities_vietnam.csv`

---

## Getting started

```bash
pip install -r requirements.txt

# Streamlit
streamlit run streamlit_app.py

# or Dash
python dash_app.py
```

---

**Hong My Ngo** · [LinkedIn](https://www.linkedin.com/in/h-my-ngo)
