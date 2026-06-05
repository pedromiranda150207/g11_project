import sqlite3
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio
from flask import render_template, session
from datafile import filename

DB_PATH = filename + 'DATABASEFINAL.db'
NAVY = '#334a94'


def _query(sql):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    con.close()
    return rows


def _to_html(fig):
    return pio.to_html(fig, full_html=False, include_plotlyjs=False,
                       config={'displayModeBar': False, 'responsive': True})


def apps_plotly():
    charts = []

    rows = list(reversed(_query("""
        SELECT substr(order_date,7,4)||'-'||substr(order_date,4,2) AS ym,
               COUNT(*) AS orders, SUM(cost) AS revenue
        FROM 'Order'
        GROUP BY ym ORDER BY ym DESC LIMIT 12
    """)))
    months  = [r[0] for r in rows]
    orders  = [r[1] for r in rows]
    revenue = [r[2] for r in rows]

    fig = make_subplots(specs=[[{'secondary_y': True}]])
    fig.add_trace(go.Bar(x=months, y=orders, name='Orders',
                         marker_color=NAVY,
                         hovertemplate='%{x}<br>Orders: %{y}<extra></extra>'),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=months, y=revenue, name='Revenue',
                             mode='lines+markers',
                             line=dict(color='#2ecc71', width=2),
                             marker=dict(size=6),
                             hovertemplate='%{x}<br>$%{y:,.0f}<extra></extra>'),
                  secondary_y=True)
    fig.update_layout(title='Monthly Orders & Revenue', paper_bgcolor='white',
                      plot_bgcolor='#f9fafd', legend=dict(x=0.01, y=0.99),
                      margin=dict(l=50, r=50, t=50, b=60), height=380)
    fig.update_yaxes(title_text='Orders', secondary_y=False, gridcolor='#eee')
    fig.update_yaxes(title_text='Revenue ($)', secondary_y=True, tickprefix='$')
    charts.append(('Monthly Orders & Revenue', _to_html(fig)))

    rows2 = _query("""
        SELECT c.name, SUM(o.cost) AS rev
        FROM 'Order' o JOIN Company c ON o.company_id = c.id
        GROUP BY c.id ORDER BY rev DESC LIMIT 10
    """)
    names2 = [r[0] for r in rows2]
    revs2  = [r[1] for r in rows2]

    fig2 = go.Figure(go.Bar(
        x=revs2, y=names2, orientation='h',
        marker=dict(color=revs2, colorscale='Blues'),
        hovertemplate='%{y}<br>$%{x:,.0f}<extra></extra>'
    ))
    fig2.update_layout(title='Top 10 Companies by Revenue',
                       paper_bgcolor='white', plot_bgcolor='#f9fafd',
                       margin=dict(l=200, r=40, t=50, b=40), height=380,
                       xaxis=dict(tickprefix='$', gridcolor='#eee'))
    charts.append(('Top 10 Companies', _to_html(fig2)))

    rows3 = _query("""
        SELECT CASE
            WHEN type LIKE '%Automated%'    THEN 'Automated'
            WHEN type LIKE '%Cold%'         THEN 'Cold Storage'
            WHEN type LIKE '%Climate%'      THEN 'Climate-Ctrl'
            WHEN type LIKE '%Regional%'     THEN 'Regional'
            WHEN type LIKE '%National%'     THEN 'National'
            WHEN type LIKE '%AI-Managed%'   THEN 'AI-Managed'
            WHEN type LIKE '%Robotic%'      THEN 'Robotic'
            WHEN type LIKE '%Distribution%' THEN 'Distribution'
            WHEN type LIKE '%Hazardous%'    THEN 'Hazardous'
            WHEN type LIKE '%Cross%'        THEN 'Cross-Dock'
            ELSE 'Other'
        END AS cat, COUNT(*) AS cnt
        FROM Warehouse GROUP BY cat ORDER BY cnt DESC
    """)
    labels3 = [r[0] for r in rows3]
    sizes3  = [r[1] for r in rows3]

    fig3 = go.Figure(go.Pie(
        labels=labels3, values=sizes3, hole=0.45,
        marker=dict(colors=px.colors.qualitative.Set2),
        hovertemplate='%{label}<br>%{value} warehouses<br>%{percent}<extra></extra>'
    ))
    fig3.update_layout(title='Warehouse Types Distribution',
                       paper_bgcolor='white',
                       margin=dict(l=20, r=20, t=50, b=20), height=380)
    charts.append(('Warehouse Types', _to_html(fig3)))

    costs = [r[0] for r in _query("SELECT cost FROM 'Order'")]

    fig4 = go.Figure(go.Histogram(
        x=costs, nbinsx=30,
        marker=dict(color='#9b59b6', opacity=0.85),
        hovertemplate='Range: %{x}<br>Orders: %{y}<extra></extra>'
    ))
    fig4.update_layout(title='Order Cost Distribution',
                       paper_bgcolor='white', plot_bgcolor='#f9fafd',
                       margin=dict(l=50, r=40, t=50, b=50), height=380,
                       xaxis=dict(title='Cost ($)', tickprefix='$', gridcolor='#eee'),
                       yaxis=dict(title='Count', gridcolor='#eee'))
    charts.append(('Cost Distribution', _to_html(fig4)))

    rows5 = _query("""
        SELECT c.name, COUNT(o.id) AS orders, SUM(o.cost) AS rev
        FROM 'Order' o JOIN Company c ON o.company_id = c.id
        GROUP BY c.id ORDER BY rev DESC LIMIT 50
    """)
    names5  = [r[0] for r in rows5]
    orders5 = [r[1] for r in rows5]
    revs5   = [r[2] for r in rows5]

    fig5 = go.Figure(go.Scatter(
        x=orders5, y=revs5, mode='markers', text=names5,
        marker=dict(size=10, color=revs5, colorscale='Viridis',
                    showscale=True, colorbar=dict(title='Revenue')),
        hovertemplate='<b>%{text}</b><br>Orders: %{x}<br>Revenue: $%{y:,.0f}<extra></extra>'
    ))
    fig5.update_layout(title='Orders vs Revenue per Company (Top 50)',
                       paper_bgcolor='white', plot_bgcolor='#f9fafd',
                       margin=dict(l=60, r=60, t=50, b=50), height=380,
                       xaxis=dict(title='Number of Orders', gridcolor='#eee'),
                       yaxis=dict(title='Total Revenue ($)', tickprefix='$', gridcolor='#eee'))
    charts.append(('Orders vs Revenue Scatter', _to_html(fig5)))

    rows6 = _query("""
        SELECT w.designation, COUNT(o.id) AS orders
        FROM 'Order' o JOIN Warehouse w ON o.warehouse_id = w.id
        GROUP BY w.id ORDER BY orders DESC LIMIT 10
    """)
    wh_names  = [r[0] for r in rows6]
    wh_orders = [r[1] for r in rows6]

    fig6 = go.Figure(go.Bar(
        x=wh_names, y=wh_orders,
        marker=dict(color='#1abc9c'),
        hovertemplate='%{x}<br>Orders: %{y}<extra></extra>'
    ))
    fig6.update_layout(title='Top 10 Warehouses by Orders',
                       paper_bgcolor='white', plot_bgcolor='#f9fafd',
                       margin=dict(l=50, r=40, t=50, b=100), height=380,
                       xaxis=dict(tickangle=-35, gridcolor='#eee'),
                       yaxis=dict(gridcolor='#eee'))
    charts.append(('Top Warehouses', _to_html(fig6)))

    return render_template('plotly_page.html', ulogin=session.get('user'), charts=charts)
