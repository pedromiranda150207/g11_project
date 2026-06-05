import sqlite3
import json
from flask import render_template, session
from datafile import filename

DB_PATH = filename + 'DATABASEFINAL.db'


def _query(sql):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    con.close()
    return rows


def apps_dashboard():
    # --- KPI cards ---
    total_orders   = _query("SELECT COUNT(*) FROM 'Order'")[0][0]
    total_revenue  = _query("SELECT SUM(cost) FROM 'Order'")[0][0] or 0
    total_companies= _query("SELECT COUNT(*) FROM Company")[0][0]
    total_warehouses=_query("SELECT COUNT(*) FROM Warehouse")[0][0]
    total_vehicles = _query("SELECT COUNT(*) FROM Vehicle")[0][0]
    avg_order_cost = round(total_revenue / total_orders, 2) if total_orders else 0

    # --- Orders & Revenue by month (last 12 months) ---
    monthly_raw = _query("""
        SELECT substr(order_date,7,4)||'-'||substr(order_date,4,2) AS ym,
               COUNT(*) AS orders,
               SUM(cost) AS revenue
        FROM 'Order'
        GROUP BY ym
        ORDER BY ym DESC
        LIMIT 12
    """)
    monthly_raw = list(reversed(monthly_raw))
    months       = [r[0] for r in monthly_raw]
    monthly_orders   = [r[1] for r in monthly_raw]
    monthly_revenue  = [r[2] for r in monthly_raw]

    # --- Top 10 companies by revenue ---
    top_companies = _query("""
        SELECT c.name, SUM(o.cost) AS revenue
        FROM 'Order' o
        JOIN Company c ON o.company_id = c.id
        GROUP BY c.id
        ORDER BY revenue DESC
        LIMIT 10
    """)
    comp_names   = [r[0] for r in top_companies]
    comp_revenue = [r[1] for r in top_companies]

    # --- Warehouse type distribution (group by base type keyword) ---
    wh_types_raw = _query("""
        SELECT CASE
            WHEN type LIKE '%Automated%'         THEN 'Automated Warehouse'
            WHEN type LIKE '%Cold%'              THEN 'Cold Storage'
            WHEN type LIKE '%Climate%'           THEN 'Climate-Controlled'
            WHEN type LIKE '%Regional%'          THEN 'Regional Logistics'
            WHEN type LIKE '%National%'          THEN 'National Storage'
            WHEN type LIKE '%AI-Managed%'        THEN 'AI-Managed Facility'
            WHEN type LIKE '%Robotic%'           THEN 'Robotic Warehouse'
            WHEN type LIKE '%Distribution%'      THEN 'Distribution Hub'
            WHEN type LIKE '%Hazardous%'         THEN 'Hazardous Materials'
            WHEN type LIKE '%Cross%'             THEN 'Cross-Docking'
            ELSE 'Other'
        END AS category,
        COUNT(*) AS cnt
        FROM Warehouse
        GROUP BY category
        ORDER BY cnt DESC
    """)
    wh_labels  = [r[0] for r in wh_types_raw]
    wh_counts  = [r[1] for r in wh_types_raw]

    # --- Top 10 warehouses by order count ---
    top_wh = _query("""
        SELECT w.designation, COUNT(o.id) AS orders
        FROM 'Order' o
        JOIN Warehouse w ON o.warehouse_id = w.id
        GROUP BY w.id
        ORDER BY orders DESC
        LIMIT 10
    """)
    wh_names  = [r[0] for r in top_wh]
    wh_orders = [r[1] for r in top_wh]

    # --- Orders per day of week ---
    dow_raw = _query("""
        SELECT substr(order_date,1,2) AS day_num, COUNT(*) AS cnt
        FROM 'Order'
        GROUP BY day_num
        ORDER BY day_num
    """)
    # Using cost distribution as histogram bins
    cost_raw = _query("SELECT cost FROM 'Order' ORDER BY cost")
    costs = [r[0] for r in cost_raw]

    # Revenue by company count (how many companies have N orders)
    orders_per_company = _query("""
        SELECT c.name, COUNT(o.id) as cnt
        FROM 'Order' o
        JOIN Company c ON o.company_id = c.id
        GROUP BY c.id
        ORDER BY cnt DESC
        LIMIT 10
    """)
    opc_names  = [r[0] for r in orders_per_company]
    opc_counts = [r[1] for r in orders_per_company]

    return render_template(
        "dashboard.html",
        ulogin=session.get("user"),
        # KPIs
        total_orders=total_orders,
        total_revenue=f"{total_revenue:,}",
        total_companies=total_companies,
        total_warehouses=total_warehouses,
        total_vehicles=total_vehicles,
        avg_order_cost=f"{avg_order_cost:,.2f}",
        # Chart data as JSON
        months=json.dumps(months),
        monthly_orders=json.dumps(monthly_orders),
        monthly_revenue=json.dumps(monthly_revenue),
        comp_names=json.dumps(comp_names),
        comp_revenue=json.dumps(comp_revenue),
        wh_labels=json.dumps(wh_labels),
        wh_counts=json.dumps(wh_counts),
        wh_names=json.dumps(wh_names),
        wh_orders=json.dumps(wh_orders),
        opc_names=json.dumps(opc_names),
        opc_counts=json.dumps(opc_counts),
        costs=json.dumps(costs),
    )
