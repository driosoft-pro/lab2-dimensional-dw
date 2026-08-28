@echo off
REM ###################################################
REM # run.bat — Run the ETL Pipeline (Windows)
REM # Usage: run.bat [--full | --schema | --load | --queries | --viz]
REM ###################################################

set SCRIPT_DIR=%~dp0
set SRC_DIR=%SCRIPT_DIR%..\src

if "%1"=="" goto :full
if "%1"=="--full" goto :full
if "%1"=="--schema" goto :schema
if "%1"=="--load" goto :load
if "%1"=="--queries" goto :queries
if "%1"=="--viz" goto :viz
if "%1"=="--help" goto :help
if "%1"=="-h" goto :help

echo Unknown option: %1
goto :help

:full
echo Running full ETL pipeline...
python "%SRC_DIR%\main.py"
goto :end

:schema
echo Creating schema...
python "%SRC_DIR%\create_schema.py"
goto :end

:load
echo Loading dimensions...
python "%SRC_DIR%\load_dimensions.py"
echo Loading fact table...
python "%SRC_DIR%\load_fact.py"
goto :end

:queries
echo Running analytical queries...
python "%SRC_DIR%\queries.py"
goto :end

:viz
echo Generating visualizations...
python "%SRC_DIR%\visualization.py"
goto :end

:help
echo Usage: %~nx0 [option]
echo.
echo Options:
echo   --full       Run the full pipeline (default)
echo   --schema     Create schema only
echo   --load       Load dimensions + facts only
echo   --queries    Run analytical queries only
echo   --viz        Generate visualizations only
echo   --help       Show this help
goto :end

:end
