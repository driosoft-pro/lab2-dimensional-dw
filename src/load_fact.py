import sqlite3
import json
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'retail_dw.db')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def get_key_mapping(conn, table, id_col, key_col):
    cursor = conn.cursor()
    cursor.execute(f"SELECT {id_col}, {key_col} FROM {table}")
    return {row[0]: row[1] for row in cursor.fetchall()}


def load_fact_sales():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Load mappings
    date_map = get_key_mapping(conn, 'DimDate', 'full_date', 'date_key')
    product_map = get_key_mapping(conn, 'DimProduct', 'product_id', 'product_key')
    store_map = get_key_mapping(conn, 'DimStore', 'store_id', 'store_key')
    channel_map = get_key_mapping(conn, 'DimChannel', 'channel_id', 'channel_key')
    promotion_map = get_key_mapping(conn, 'DimPromotion', 'promotion_id', 'promotion_key')

    # Load product list prices for gross_sales calculation
    cursor.execute("SELECT product_id, list_price, unit_cost FROM DimProduct")
    product_prices = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}

    # Load promotion discount
    cursor.execute("SELECT promotion_id, discount_pct FROM DimPromotion")
    promo_discounts = {row[0]: row[1] for row in cursor.fetchall()}

    # Read sales data
    sales_df = pd.read_csv(os.path.join(DATA_DIR, 'sales_transactions.csv'))

    count = 0
    for _, row in sales_df.iterrows():
        date_key = int(pd.to_datetime(row['sale_date']).strftime('%Y%m%d'))
        product_key = product_map.get(row['product_id'])
        store_key = store_map.get(row['store_id'])
        channel_key = channel_map.get(row['channel_id'])
        promotion_key = promotion_map.get(row['promotion_id'])

        if None in (product_key, store_key, channel_key, promotion_key):
            continue

        quantity = row['quantity']
        unit_price_sale = row['unit_price_sale']
        list_price, unit_cost = product_prices[row['product_id']]

        gross_sales = quantity * list_price
        net_sales = quantity * unit_price_sale
        discount_amount = gross_sales - net_sales
        cost_amount = quantity * unit_cost
        gross_profit = net_sales - cost_amount

        cursor.execute(
            "INSERT INTO FactSales "
            "(date_key, product_key, store_key, channel_key, promotion_key, "
            "quantity, gross_sales, net_sales, discount_amount, cost_amount, gross_profit) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (date_key, product_key, store_key, channel_key, promotion_key,
             quantity, gross_sales, net_sales, discount_amount, cost_amount, gross_profit)
        )
        count += 1

    conn.commit()
    conn.close()
    print(f"[OK] FactSales loaded ({count} rows)")


if __name__ == "__main__":
    load_fact_sales()
