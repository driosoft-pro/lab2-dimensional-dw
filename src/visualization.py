import sqlite3
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'retail_dw.db')
DOCS_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')


def visualization_monthly_sales():
    """Visualization 1: Monthly Net Sales Trend (Temporal - Line Chart)"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT d.month_name, d.month, SUM(f.net_sales) AS total_net_sales
        FROM FactSales f
        JOIN DimDate d ON f.date_key = d.date_key
        GROUP BY d.month_name, d.month
        ORDER BY d.month;
    """, conn)
    conn.close()

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df['month_name'], df['total_net_sales'], marker='o', linewidth=2, color='#2196F3')
    ax.set_title('R1: Monthly Net Sales Trend (Jan-Jun 2026)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Month')
    ax.set_ylabel('Net Sales (COP)')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(DOCS_DIR, 'visualization_monthly_sales.png'), dpi=150)
    plt.close()
    print("[OK] Visualization 1 saved: visualization_monthly_sales.png")


def visualization_sales_by_store():
    """Visualization 2: Sales by Store and Channel (Comparative - Bar Chart)"""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT s.store_name, c.channel_name, SUM(f.net_sales) AS total_net_sales
        FROM FactSales f
        JOIN DimStore s ON f.store_key = s.store_key
        JOIN DimChannel c ON f.channel_key = c.channel_key
        GROUP BY s.store_name, c.channel_name
        ORDER BY total_net_sales DESC;
    """, conn)
    conn.close()

    fig, ax = plt.subplots(figsize=(10, 5))
    labels = [f"{row['store_name']}\n({row['channel_name']})" for _, row in df.iterrows()]
    bars = ax.bar(labels, df['total_net_sales'], color=['#4CAF50', '#FF9800', '#E91E63'])
    ax.set_title('R2: Sales Performance by Store and Channel', fontsize=14, fontweight='bold')
    ax.set_ylabel('Net Sales (COP)')
    ax.set_xlabel('Store / Channel')
    for bar, val in zip(bars, df['total_net_sales']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1000,
                f'{val:,.0f}', ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(DOCS_DIR, 'visualization_sales_by_store.png'), dpi=150)
    plt.close()
    print("[OK] Visualization 2 saved: visualization_sales_by_store.png")


if __name__ == "__main__":
    visualization_monthly_sales()
    visualization_sales_by_store()
