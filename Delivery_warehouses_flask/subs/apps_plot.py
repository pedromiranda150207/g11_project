import sqlite3
import base64
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
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


def _fig_to_b64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=110)
    buf.seek(0)
    data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return data


def apps_plot():
    charts = []

    rows = list(reversed(_query("""
        SELECT substr(order_date,7,4)||'-'||substr(order_date,4,2) AS ym,
               COUNT(*) AS cnt
        FROM 'Order'
        GROUP BY ym ORDER BY ym DESC LIMIT 12
    """)))
    months = [r[0] for r in rows]
    counts = [r[1] for r in rows]

    fig, ax = plt.subplots(figsize=(8, 4))
    bars = ax.bar(months, counts, color=NAVY, width=0.6)
    ax.set_title('Monthly Orders (Last 12 Months)', fontweight='bold', color=NAVY)
    ax.set_xlabel('Month')
    ax.set_ylabel('Orders')
    ax.set_xticklabels(months, rotation=35, ha='right', fontsize=8)
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_facecolor('#f9fafd')
    fig.patch.set_facecolor('#ffffff')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 2,
                str(int(bar.get_height())), ha='center', va='bottom', fontsize=7)
    charts.append(('Monthly Orders', _fig_to_b64(fig)))

    rows2 = list(reversed(_query("""
        SELECT substr(order_date,7,4)||'-'||substr(order_date,4,2) AS ym,
               SUM(cost) AS revenue
        FROM 'Order'
        GROUP BY ym ORDER BY ym DESC LIMIT 12
    """)))
    months2  = [r[0] for r in rows2]
    revenues = [r[1] for r in rows2]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(months2, revenues, color='#2ecc71', linewidth=2.5, marker='o',
            markersize=5, markerfacecolor='#27ae60')
    ax.fill_between(range(len(months2)), revenues, alpha=0.15, color='#2ecc71')
    ax.set_xticks(range(len(months2)))
    ax.set_xticklabels(months2, rotation=35, ha='right', fontsize=8)
    ax.set_title('Monthly Revenue (Last 12 Months)', fontweight='bold', color=NAVY)
    ax.set_xlabel('Month')
    ax.set_ylabel('Revenue ($)')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e3:.0f}k'))
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_facecolor('#f9fafd')
    fig.patch.set_facecolor('#ffffff')
    charts.append(('Monthly Revenue', _fig_to_b64(fig)))

    rows3 = _query("""
        SELECT c.name, SUM(o.cost) AS rev
        FROM 'Order' o JOIN Company c ON o.company_id = c.id
        GROUP BY c.id ORDER BY rev DESC LIMIT 10
    """)
    names3 = [r[0] for r in reversed(rows3)]
    revs3  = [r[1] for r in reversed(rows3)]
    colors = ['#334a94','#3d5cbf','#4a6fd4','#5780e0','#2ecc71',
              '#27ae60','#9b59b6','#8e44ad','#e67e22','#d35400']

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.barh(names3, revs3, color=colors)
    ax.set_title('Top 10 Companies by Revenue', fontweight='bold', color=NAVY)
    ax.set_xlabel('Revenue ($)')
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x/1e3:.0f}k'))
    ax.spines[['top', 'right']].set_visible(False)
    ax.set_facecolor('#f9fafd')
    fig.patch.set_facecolor('#ffffff')
    for bar in bars:
        ax.text(bar.get_width() + 500, bar.get_y() + bar.get_height() / 2,
                f'${bar.get_width()/1e3:.1f}k', va='center', fontsize=8)
    charts.append(('Top 10 Companies', _fig_to_b64(fig)))

    rows4 = _query("""
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
    labels4 = [r[0] for r in rows4]
    sizes4  = [r[1] for r in rows4]
    pie_colors = ['#334a94','#2ecc71','#9b59b6','#e67e22','#1abc9c',
                  '#e74c3c','#3498db','#f39c12','#16a085','#8e44ad','#95a5a6']

    fig, ax = plt.subplots(figsize=(7, 5))
    wedges, texts, autotexts = ax.pie(
        sizes4, colors=pie_colors[:len(sizes4)],
        autopct='%1.1f%%', startangle=140, pctdistance=0.75,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
    )
    for at in autotexts:
        at.set_fontsize(7)
    ax.legend(wedges, labels4, loc='center left', bbox_to_anchor=(0.85, 0.5),
              fontsize=7, frameon=False)
    ax.set_title('Warehouse Types Distribution', fontweight='bold', color=NAVY)
    fig.patch.set_facecolor('#ffffff')
    charts.append(('Warehouse Types', _fig_to_b64(fig)))

    return render_template('plot.html', ulogin=session.get('user'), charts=charts)
