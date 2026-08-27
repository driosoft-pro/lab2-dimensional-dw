import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'retail_dw.db')

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS DimDate (
    date_key    INTEGER PRIMARY KEY,
    full_date   TEXT NOT NULL,
    day         INTEGER,
    month       INTEGER,
    year        INTEGER,
    month_name  TEXT
);

CREATE TABLE IF NOT EXISTS DimProduct (
    product_key  INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id   TEXT NOT NULL,
    product_name TEXT,
    category     TEXT,
    brand        TEXT,
    list_price   REAL,
    unit_cost    REAL
);

CREATE TABLE IF NOT EXISTS DimStore (
    store_key   INTEGER PRIMARY KEY AUTOINCREMENT,
    store_id    TEXT NOT NULL,
    store_name  TEXT,
    city        TEXT,
    region      TEXT,
    channel_id  TEXT
);

CREATE TABLE IF NOT EXISTS DimChannel (
    channel_key  INTEGER PRIMARY KEY AUTOINCREMENT,
    channel_id   TEXT NOT NULL,
    channel_name TEXT
);

CREATE TABLE IF NOT EXISTS DimPromotion (
    promotion_key   INTEGER PRIMARY KEY AUTOINCREMENT,
    promotion_id    TEXT NOT NULL,
    promotion_name  TEXT,
    discount_pct    REAL
);

CREATE TABLE IF NOT EXISTS FactSales (
    sale_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    date_key         INTEGER NOT NULL,
    product_key      INTEGER NOT NULL,
    store_key        INTEGER NOT NULL,
    channel_key      INTEGER NOT NULL,
    promotion_key    INTEGER NOT NULL,
    quantity         INTEGER,
    gross_sales      REAL,
    net_sales        REAL,
    discount_amount  REAL,
    cost_amount      REAL,
    gross_profit     REAL,
    FOREIGN KEY (date_key)      REFERENCES DimDate(date_key),
    FOREIGN KEY (product_key)   REFERENCES DimProduct(product_key),
    FOREIGN KEY (store_key)     REFERENCES DimStore(store_key),
    FOREIGN KEY (channel_key)   REFERENCES DimChannel(channel_key),
    FOREIGN KEY (promotion_key) REFERENCES DimPromotion(promotion_key)
);
"""


def create_schema():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()
    print(f"[OK] Schema created in {DB_PATH}")


if __name__ == "__main__":
    create_schema()
