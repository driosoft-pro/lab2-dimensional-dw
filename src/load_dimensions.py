import sqlite3
import json
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'retail_dw.db')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')


def load_dim_date(conn):
    df = pd.read_csv(os.path.join(DATA_DIR, 'sales_transactions.csv'))
    dates = pd.to_datetime(df['sale_date']).dt.date.unique()
    cursor = conn.cursor()
    for d in sorted(dates):
        cursor.execute(
            "INSERT OR IGNORE INTO DimDate (date_key, full_date, day, month, year, month_name) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (int(d.strftime('%Y%m%d')), str(d), d.day, d.month, d.year, d.strftime('%B'))
        )
    conn.commit()
    print(f"[OK] DimDate loaded ({len(dates)} dates)")


def load_dim_product(conn):
    with open(os.path.join(DATA_DIR, 'reference_data.json'), 'r') as f:
        ref = json.load(f)
    cursor = conn.cursor()
    for p in ref['products']:
        cursor.execute(
            "INSERT INTO DimProduct (product_id, product_name, category, brand, list_price, unit_cost) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (p['product_id'], p['product_name'], p['category'], p['brand'], p['list_price'], p['unit_cost'])
        )
    conn.commit()
    print(f"[OK] DimProduct loaded ({len(ref['products'])} products)")


def load_dim_store(conn):
    with open(os.path.join(DATA_DIR, 'reference_data.json'), 'r') as f:
        ref = json.load(f)
    cursor = conn.cursor()
    for s in ref['stores']:
        cursor.execute(
            "INSERT INTO DimStore (store_id, store_name, city, region, channel_id) "
            "VALUES (?, ?, ?, ?, ?)",
            (s['store_id'], s['store_name'], s['city'], s['region'], s['channel_id'])
        )
    conn.commit()
    print(f"[OK] DimStore loaded ({len(ref['stores'])} stores)")


def load_dim_channel(conn):
    with open(os.path.join(DATA_DIR, 'reference_data.json'), 'r') as f:
        ref = json.load(f)
    cursor = conn.cursor()
    for c in ref['channels']:
        cursor.execute(
            "INSERT INTO DimChannel (channel_id, channel_name) VALUES (?, ?)",
            (c['channel_id'], c['channel_name'])
        )
    conn.commit()
    print(f"[OK] DimChannel loaded ({len(ref['channels'])} channels)")


def load_dim_promotion(conn):
    with open(os.path.join(DATA_DIR, 'reference_data.json'), 'r') as f:
        ref = json.load(f)
    cursor = conn.cursor()
    for pr in ref['promotions']:
        cursor.execute(
            "INSERT INTO DimPromotion (promotion_id, promotion_name, discount_pct) VALUES (?, ?, ?)",
            (pr['promotion_id'], pr['promotion_name'], pr['discount_pct'])
        )
    conn.commit()
    print(f"[OK] DimPromotion loaded ({len(ref['promotions'])} promotions)")


def load_all_dimensions():
    conn = sqlite3.connect(DB_PATH)
    load_dim_date(conn)
    load_dim_product(conn)
    load_dim_store(conn)
    load_dim_channel(conn)
    load_dim_promotion(conn)
    conn.close()


if __name__ == "__main__":
    load_all_dimensions()
