#!/usr/bin/env python3
"""
Lab 2 — Dimensional Data Warehouse: Retail Technology Sales
ETL (G01) — Universidad EAFIT

Main entry point: creates schema, loads dimensions, loads facts,
runs queries, and generates visualizations.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from create_schema import create_schema
from load_dimensions import load_all_dimensions
from load_fact import load_fact_sales
from queries import run_queries
from visualization import visualization_monthly_sales, visualization_sales_by_store


def main():
    print("=" * 60)
    print("  Lab 2 — Dimensional Data Warehouse Pipeline")
    print("=" * 60)

    # Step 1: Create schema
    print("\n[Step 1/5] Creating schema...")
    create_schema()

    # Step 2: Load dimensions
    print("\n[Step 2/5] Loading dimensions...")
    load_all_dimensions()

    # Step 3: Load fact table
    print("\n[Step 3/5] Loading fact table...")
    load_fact_sales()

    # Step 4: Run analytical queries
    print("\n[Step 4/5] Running analytical queries (R1-R5)...")
    run_queries()

    # Step 5: Generate visualizations
    print("\n[Step 5/5] Generating visualizations...")
    visualization_monthly_sales()
    visualization_sales_by_store()

    print("\n" + "=" * 60)
    print("  Pipeline completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
