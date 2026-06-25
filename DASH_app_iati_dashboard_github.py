# Deine Imports:
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from dash import Dash, html, dcc, Input, Output, dash_table
import plotly.express as px

# Datensatz laden:
iati_activities = pd.read_csv(
    r"data/IATI_activities_vietnam.csv",
    index_col=0
)

print(iati_activities.head())

print(iati_activities.columns.tolist())

# ---------------------------
# 1. Daten laden
# ---------------------------
iati_activities = pd.read_csv(
    r"data/IATI_activities_vietnam.csv" 
)

# ---------------------------
# 2. Vorbereitung
# ---------------------------

# Jahr aus Datum extrahieren
iati_activities['year'] = pd.to_datetime(
    iati_activities['day_start'],
    errors='coerce'
).dt.year

# Organisationen für Dropdown
orgs = sorted(iati_activities['reporting'].dropna().unique())

# ---------------------------
# 3. App starten
# ---------------------------
app = Dash(__name__)

# ---------------------------
# 4. Layout
# ---------------------------
app.layout = html.Div(
    style={'backgroundColor': "#ffffff", 'padding': '20px'},
    children=[

        html.H1(
            "Vietnam IATI (International Aid Transparency Initiative) Dashboard",
            style={
                'textAlign': 'center',
                'color': "#052691",
                'marginBottom': '20px',
                'fontFamily': 'Segoe UI'
            }
        ),

        dcc.Dropdown(
            options=orgs,
            value=orgs[0],
            id='org-dropdown'
        ),

        html.Hr(),

        html.Div(id='kpi-box'
                 ),

        html.Hr(),

        html.Div([
            dcc.Graph(id='sector-graph')
        ]),

        html.Hr(style={
            # 'border': '1px solid #052691',
            'marginTop': '20px',
            'marginBottom': '20px'
        }),

        html.Div([
            dcc.Graph(id='status-graph', style={'width': '80%'}),
            dcc.Graph(id='budget-scatter', style={'width': '80%'}),
            dcc.Graph(id='time-graph', style={'width': '80%'}),
        ], style={'display': 'flex', 'gap': '20px'}),

        html.Hr(),

        html.H2(
            "Projektübersicht",
            style={
                'textAlign': 'left',
                'color': "#052691",
                'marginTop': '15px',
                'fontFamily': 'Segoe UI'
            }
        ),
        dash_table.DataTable(
            id='table',
            page_size=8,
            style_cell={'textAlign': 'left'},
            style_table={'overflowX': 'auto'}
        )
    ]
)

# ---------------------------
# 5. Callback
# ---------------------------
@app.callback(
    Output('sector-graph', 'figure'),
    Output('status-graph', 'figure'),
    Output('budget-scatter', 'figure'),
    Output('time-graph', 'figure'),
    Output('table', 'data'),
    Output('kpi-box', 'children'),
    Input('org-dropdown', 'value')
)
def update_dashboard(org):

    df = iati_activities[iati_activities['reporting'] == org]

    # ---------------- KPI ----------------
    total_budget = df['commitment_eur'].sum()
    total_spend = df['spend_eur'].sum()
    projects = df.shape[0]

    kpis = html.Div([
        html.H3(f"Projekte: {projects}"),
        html.H3(f"Budget: €{total_budget:,.0f}"),
        html.H3(f" bisherige Ausgaben: €{total_spend:,.0f}")
    ], style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'fontFamily': 'Segoe UI',
        'color': "#070591"
    })

    # ---------------- Sector ----------------
    sector = df.groupby('sector_group')['commitment_eur'].sum().reset_index()

    fig_sector = px.bar(
        sector,
        x='sector_group',
        y='commitment_eur',
        title="Sektorverteilung",
        color_discrete_sequence=["#052691"]
    )

    fig_sector.update_traces(
        text=sector['commitment_eur'],
        texttemplate='%{text:,.0f}',
        textposition='outside'
    )

    fig_sector.update_layout(
        yaxis_title="Projektbudget in Mio €",
        xaxis_title="Sektor"
    )

    # ---------------- Status ----------------
    fig_status = px.pie(
        df,
        names='status_code',
        title="Projektstatus"
    )

    # ---------------- Budget vs Spend ----------------
    fig_scatter = px.scatter(
        df,
        x='commitment_eur',
        y='spend_eur',
        color='status_code',
        title="Budget vs Ausgaben",
        labels={'status_code': 'Status'}
    )
    fig_scatter.update_layout(
        yaxis_title="bisherige Ausgaben in Mio €",
        xaxis_title="Projektbudget in Mio €"
    )
    # ---------------- Zeit ----------------
    time = df.groupby('year')['commitment_eur'].sum().reset_index()

    fig_time = px.line(
        time,
        x='year',
        y='commitment_eur',
        title="Entwicklung über Zeit",
        color_discrete_sequence=["#052691"]
    )

    fig_time.update_layout(
        yaxis_title="Projektbudget in Mio €",
        xaxis_title="Jahr"
    )

    # ---------------- Table ----------------
    table_data = df[
        ['title', 'sector_group', 'commitment_eur', 'spend_eur', 'status_code']
    ].to_dict('records')

    return fig_sector, fig_status, fig_scatter, fig_time, table_data, kpis


# ---------------------------
# 6. Start
# ---------------------------
if __name__ == '__main__':
    app.run(debug=True)
