# Vietnam Development Aid Dashboard

### IATI Data Analysis · Python · Dash · Streamlit · Plotly

This project analyzes development aid projects in Vietnam using publicly available data from the International Aid Transparency Initiative (IATI).

Two interactive dashboards were developed: one using Dash and the other using Streamlit, each designed to visualize different aspects of development cooperation in Vietnam.

---

## Contents

| File               | Description                                           |
| ------------------ | ----------------------------------------------------- |
| `streamlit_app.py` | Streamlit dashboard with sidebar filters              |
| `dash_app.py`      | Dash dashboard featuring dropdown menus and callbacks |
| `requirements.txt` | Required Python packages                              |

---

## What the dashboards show

* **KPIs:** Number of projects, total budget, expenditures to date, and budget utilization
* **Sector Distribution:** Top 10 funded sectors by budget allocation
* **Project Status:** Active, completed, and planned projects
* **Time Trends:** Budget development over time
* **Budget vs. Expenditures:** Scatter plot illustrating fund utilization
* **Data Quality:** Missing values by variable

---

## Data

The raw data is provided by the International Aid Transparency Initiative (IATI) and is not included in this repository due to licensing restrictions.

To download the dataset:

1. Visit the IATI country data portal for Vietnam
2. Download the dataset **"IATI activities in Viet Nam"** as a CSV file
3. Save the file as `data/IATI_activities_vietnam.csv`

---

## Installation & Usage

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/iati-vietnam-analysis.git
cd iati-vietnam-analysis

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit dashboard
streamlit run streamlit_app.py

# Or run the Dash dashboard
python dash_app.py
```

---

## Technologies

`Python` · `pandas` · `Plotly` · `Dash` · `Streamlit`

---

## Author

**My Ngo** · [LinkedIn](https://www.linkedin.com/in/h-my-ngo)

GitHub: https://github.com/hongmy-ngo
