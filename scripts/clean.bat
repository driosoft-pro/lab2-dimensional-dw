@echo off
REM ###################################################
REM # clean.bat — Remove generated files (Windows)
REM ###################################################

echo Cleaning generated files...

if exist .venv rmdir /s /q .venv
if exist database\retail_dw.db del database\retail_dw.db
if exist docs\visualization_monthly_sales.png del docs\visualization_monthly_sales.png
if exist docs\visualization_sales_by_store.png del docs\visualization_sales_by_store.png
if exist src\__pycache__ rmdir /s /q src\__pycache__

echo Done.
