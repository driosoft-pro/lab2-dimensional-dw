import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'retail_dw.db')

QUERIES = {
    "R1 - Monthly Net Sales Trend": """
        SELECT d.year, d.month, d.month_name,
               SUM(f.net_sales) AS total_net_sales
        FROM FactSales f
        JOIN DimDate d ON f.date_key = d.date_key
        GROUP BY d.year, d.month, d.month_name
        ORDER BY d.year, d.month;
    """,
    "R2 - Sales by Store and Channel": """
        SELECT s.store_name, c.channel_name,
               SUM(f.net_sales) AS total_net_sales
        FROM FactSales f
        JOIN DimStore s ON f.store_key = s.store_key
        JOIN DimChannel c ON f.channel_key = c.channel_key
        GROUP BY s.store_name, c.channel_name
        ORDER BY total_net_sales DESC;
    """,
    "R3 - Top Categories and Brands": """
        SELECT p.category, p.brand,
               SUM(f.net_sales) AS total_revenue,
               SUM(f.quantity) AS total_units
        FROM FactSales f
        JOIN DimProduct p ON f.product_key = p.product_key
        GROUP BY p.category, p.brand
        ORDER BY total_revenue DESC;
    """,
    "R4 - Promotion Performance": """
        SELECT pr.promotion_name, pr.discount_pct,
               SUM(f.net_sales) AS total_sales,
               SUM(f.quantity) AS total_units,
               SUM(f.discount_amount) AS total_discount
        FROM FactSales f
        JOIN DimPromotion pr ON f.promotion_key = pr.promotion_key
        GROUP BY pr.promotion_name, pr.discount_pct
        ORDER BY total_sales DESC;
    """,
    "R5 - Gross Profit and Margin": """
        SELECT p.category, s.store_name, d.month_name,
               SUM(f.gross_profit) AS total_gross_profit,
               ROUND(SUM(f.gross_profit) / SUM(f.net_sales) * 100, 2) AS gross_margin_pct
        FROM FactSales f
        JOIN DimProduct p ON f.product_key = p.product_key
        JOIN DimStore s ON f.store_key = s.store_key
        JOIN DimDate d ON f.date_key = d.date_key
        GROUP BY p.category, s.store_name, d.month_name
        ORDER BY gross_margin_pct DESC;
    """
}


def run_queries():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for title, sql in QUERIES.items():
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        # Print header
        header = " | ".join(f"{col:>20}" for col in columns)
        print(header)
        print("-" * len(header))

        # Print rows
        for row in rows:
            print(" | ".join(f"{str(val):>20}" for val in row))

    conn.close()


if __name__ == "__main__":
    run_queries()
