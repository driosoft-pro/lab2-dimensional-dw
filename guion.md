# Guion de Presentación — Lab 2: Dimensional Data Warehouse

> **ETL (G01) — Universidad Autonoma de Occidente**
> Duración estimada: 20-25 minutos

---

## Estructura de la Presentación

| Sección | Tiempo | Responsable |
|---------|--------|-------------|
| 1. Introducción y Contexto | 2 min | Deyton Riascos |
| 2. Arquitectura del Sistema | 3 min | Deyton Riascos |
| 3. Diseño del Modelo Dimensional | 4 min | Samuel Izquierdo |
| 4. Implementación del Pipeline ETL | 4 min | Deyton Riascos |
| 5. Queries Analíticos y KPIs | 3 min | Daniel García |
| 6. Visualizaciones y Resultados | 3 min | Mauricio Taborda |
| 7. Conclusiones y Reflexión | 2 min | Daniel García |
| **Total** | **21 min** | |

---

## 1. Introducción y Contexto (Deyton — 2 min)

### Diálogo sugerido:

> "Buenos días. Nuestro proyecto consiste en diseñar e implementar un Data Warehouse dimensional para una empresa de retail tecnológico que opera dos tiendas físicas y una tienda online a nivel nacional.
>
> El objetivo es consolidar seis meses de datos de ventas (enero a junio 2026) en un modelo Star Schema que soporte consultas analíticas recurrentes y futuros dashboards.
>
> El dataset contiene 1,000 líneas de venta, 4 categorías de productos, 4 marcas, y múltiples condiciones de promoción."

### Puntos clave a mencionar:
- Empresa de retail tecnológico (2 tiendas físicas + 1 online)
- Periodo: enero - junio 2026
- 1,000 líneas de venta
- 5 requisitos de negocio (R1-R5)

---

## 2. Arquitectura del Sistema (Deyton — 3 min)

### Diagrama de Arquitectura General

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            SISTEMA COMPLETO                                       │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                         FUENTES DE DATOS                                    │  │
│  │                                                                             │  │
│  │  ┌────────────────────────┐       ┌────────────────────────┐                │  │
│  │  │ sales_transactions.csv │       │ reference_data.json    │                │  │
│  │  │                        │       │                        │                │  │
│  │  │ • 1,000 filas          │       │ • products (8)         │                │  │
│  │  │ • sale_line_id         │       │ • stores (3)           │                │  │
│  │  │ • transaction_id       │       │ • channels (3)         │                │  │
│  │  │ • sale_date            │       │ • promotions (6)       │                │  │
│  │  │ • store_id             │       │                        │                │  │
│  │  │ • product_id           │       └────────────────────────┘                │  │
│  │  │ • channel_id           │                                                 │  │
│  │  │ • promotion_id         │                                                 │  │
│  │  │ • quantity             │                                                 │  │
│  │  │ • unit_price_sale      │                                                 │  │
│  │  └────────────────────────┘                                                 │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                            │
│                                      ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                         PIPELINE ETL                                         │  │
│  │                                                                             │  │
│  │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │  │
│  │  │   EXTRACT    │───►│  TRANSFORM   │───►│     LOAD     │                   │  │
│  │  │              │    │              │    │              │                   │  │
│  │  │ • Leer CSV   │    │ • Map IDs    │    │ • Dimensions │                   │  │
│  │  │ • Leer JSON  │    │ • Calc KPIs  │    │ • Fact Table │                   │  │
│  │  │ • Validar    │    │ • Surrogate  │    │ • FK constr. │                   │  │
│  │  └──────────────┘    │   Keys       │    └──────┬───────┘                   │  │
│  │                      └──────────────┘           │                           │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                            │
│                                      ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                      DATA WAREHOUSE (SQLite)                                 │  │
│  │                                                                             │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐          │  │
│  │  │ DimDate  │ │DimProduct│ │ DimStore │ │DimChannel│ │DimPromo  │          │  │
│  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘          │  │
│  │       │             │            │             │             │               │  │
│  │       └─────────────┴────────────┼─────────────┴─────────────┘               │  │
│  │                                  │                                           │  │
│  │                          ┌───────┴───────┐                                   │  │
│  │                          │  FactSales    │                                   │  │
│  │                          │  (1,000 rows) │                                   │  │
│  │                          └───────────────┘                                   │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│                                      │                                            │
│                                      ▼                                            │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                         SALIDAS                                               │  │
│  │                                                                             │  │
│  │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐           │  │
│  │  │ SQL Queries R1-R5│  │ Visualizaciones  │  │   Notebook       │           │  │
│  │  │ (Consola)        │  │ (PNG en docs/)   │  │  (Interactivo)   │           │  │
│  │  └──────────────────┘  └──────────────────┘  └──────────────────┘           │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Flujo de Datos Detallado

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           FLUJO DE DATOS                                         │
│                                                                                   │
│  PASO 1: EXTRACT                                                                 │
│  ┌─────────────────┐     ┌─────────────────┐                                     │
│  │ CSV (1,000 filas)│     │ JSON (referencia)│                                     │
│  │ • sale_date      │     │ • products       │                                     │
│  │ • store_id       │     │ • stores         │                                     │
│  │ • product_id     │     │ • channels       │                                     │
│  │ • channel_id     │     │ • promotions     │                                     │
│  │ • promotion_id   │     └─────────────────┘                                     │
│  │ • quantity       │                                                             │
│  │ • unit_price_sale│                                                             │
│  └─────────────────┘                                                             │
│         │                                                                        │
│         ▼                                                                        │
│  PASO 2: TRANSFORM                                                               │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                             │  │
│  │  Mapeo de IDs a Surrogate Keys:                                             │  │
│  │  ┌──────────────┐    ┌──────────────┐                                       │  │
│  │  │ product_id   │───►│ product_key  │  (DimProduct)                         │  │
│  │  │ store_id     │───►│ store_key    │  (DimStore)                           │  │
│  │  │ channel_id   │───►│ channel_key  │  (DimChannel)                         │  │
│  │  │ promotion_id │───►│ promotion_key│  (DimPromotion)                       │  │
│  │  │ sale_date    │───►│ date_key     │  (DimDate: YYYYMMDD)                  │  │
│  │  └──────────────┘    └──────────────┘                                       │  │
│  │                                                                             │  │
│  │  Cálculo de Medidas:                                                         │  │
│  │  ┌───────────────────────────────────────────────────────────────────────┐   │  │
│  │  │ gross_sales      = quantity × list_price                             │   │  │
│  │  │ net_sales        = quantity × unit_price_sale                        │   │  │
│  │  │ discount_amount  = gross_sales − net_sales                           │   │  │
│  │  │ cost_amount      = quantity × unit_cost                              │   │  │
│  │  │ gross_profit     = net_sales − cost_amount                           │   │  │
│  │  └───────────────────────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│         │                                                                        │
│         ▼                                                                        │
│  PASO 3: LOAD                                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                             │  │
│  │  Orden de Carga (respetando FK):                                            │  │
│  │                                                                             │  │
│  │  1. DimDate       ← Generado de sale_date (181 fechas)                     │  │
│  │  2. DimProduct    ← reference_data.json → products (8 productos)            │  │
│  │  3. DimStore      ← reference_data.json → stores (3 tiendas)               │  │
│  │  4. DimChannel    ← reference_data.json → channels (3 canales)             │  │
│  │  5. DimPromotion  ← reference_data.json → promotions (6 promos)            │  │
│  │  6. FactSales     ← sales_transactions.csv (1,000 filas)                   │  │
│  │                                                                             │  │
│  │  ┌───────────────────────────────────────────────────────────────────────┐   │  │
│  │  │ SQLite Database: database/retail_dw.db                               │   │  │
│  │  │ • 5 tablas de dimensión                                              │   │  │
│  │  │ • 1 tabla de hechos                                                  │   │  │
│  │  │ • PK/FK constraints enforced                                         │   │  │
│  │  └───────────────────────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
│         │                                                                        │
│         ▼                                                                        │
│  PASO 4: QUERY & VISUALIZE                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────────┐  │
│  │                                                                             │  │
│  │  Queries Analíticas:                                                        │  │
│  │  ┌───────────────────────────────────────────────────────────────────────┐   │  │
│  │  │ R1: Tendencia mensual de ventas netas                                │   │  │
│  │  │ R2: Ventas por tienda y canal                                        │   │  │
│  │  │ R3: Top categorías y marcas                                          │   │  │
│  │  │ R4: Rendimiento de promociones                                       │   │  │
│  │  │ R5: Margen bruto por categoría/tienda/mes                            │   │  │
│  │  └───────────────────────────────────────────────────────────────────────┘   │  │
│  │                                                                             │  │
│  │  Visualizaciones:                                                           │  │
│  │  ┌───────────────────────────────────────────────────────────────────────┐   │  │
│  │  │ V1: Line chart — Tendencia mensual (R1)                              │   │  │
│  │  │ V2: Bar chart — Ventas por tienda/canal (R2)                         │   │  │
│  │  └───────────────────────────────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Estructura del Repositorio

```
lab2-dimensional-dw/
├── flake.nix                    # Entorno NixOS (Python 3.12 + uv + Jupyter)
├── requirements.txt             # Dependencias Python
├── guion.md                     # Guion de presentación (este archivo)
├── README.md                    # Documentación completa
│
├── scripts/                     # Scripts de ejecución
│   ├── run.sh                   # Ejecutar pipeline (Linux/macOS)
│   ├── run.bat                  # Ejecutar pipeline (Windows)
│   ├── setup.sh                 # Configurar entorno (Linux/macOS)
│   ├── setup.bat                # Configurar entorno (Windows)
│   ├── clean.sh                 # Limpiar archivos generados (Linux/macOS)
│   └── clean.bat                # Limpiar archivos generados (Windows)
│
├── data/                        # Fuentes de datos
│   ├── sales_transactions.csv   # 1,000 líneas de venta
│   ├── reference_data.json      # Productos, tiendas, canales, promos
│   └── DATA_DICTIONARY.md       # Diccionario de datos
│
├── src/                         # Código fuente ETL
│   ├── main.py                  # Orquestador principal
│   ├── create_schema.py         # DDL del Star Schema
│   ├── load_dimensions.py       # Carga de 5 dimensiones
│   ├── load_fact.py             # Carga de FactSales
│   ├── queries.py               # Queries R1-R5
│   └── visualization.py         # Generación de gráficos
│
├── database/                    # Data Warehouse generado
│   └── retail_dw.db             # SQLite database
│
├── notebooks/                   # Notebooks interactivos
│   └── 01_dimensional_modeling.ipynb
│
└── docs/                        # Documentación y salidas
    ├── plan.md                  # Plan del proyecto
    ├── visualization_monthly_sales.png
    └── visualization_sales_by_store.png
```

### Script de Ejecución

```bash
# Opción 1: Pipeline completo
python src/main.py

# Opción 2: Usando scripts
./scripts/run.sh              # Pipeline completo
./scripts/run.sh --schema     # Solo crear esquema
./scripts/run.sh --load       # Solo cargar datos
./scripts/run.sh --queries    # Solo ejecutar queries
./scripts/run.sh --viz        # Solo generar visualizaciones

# Opción 3: Windows
scripts\run.bat              # Pipeline completo
scripts\run.bat --schema     # Solo crear esquema

# Opción 4: Notebook interactivo
jupyter lab notebooks/01_dimensional_modeling.ipynb
```

### Diálogo sugerido:

> "La arquitectura del sistema sigue un flujo ETL claro y documentado.
>
> **Fuentes de datos:** Tenemos dos archivos — `sales_transactions.csv` con 1,000 líneas de venta, y `reference_data.json` con la referencia de productos, tiendas, canales y promociones.
>
> **Pipeline ETL:** El flujo tiene cuatro pasos:
> 1. **Extract:** Leemos ambos archivos y validamos la estructura.
> 2. **Transform:** Mapeamos los IDs naturales a surrogate keys y calculamos las cinco medidas de negocio.
> 3. **Load:** Cargamos en orden correcto — primero las 5 dimensiones, luego la tabla de hechos, respetando las restricciones de integridad referencial.
> 4. **Query & Visualize:** Ejecutamos las 5 queries analíticas y generamos 2 visualizaciones.
>
> **Salida:** La base de datos SQLite se genera en `database/retail_dw.db`, y los gráficos se guardan en `docs/`.
>
> El pipeline completo se ejecuta con un solo comando: `python src/main.py`."

### Puntos clave a mencionar:
- Arquitectura ETL clara y documentada
- Dos fuentes de datos (CSV + JSON)
- Pipeline en 4 pasos: Extract → Transform → Load → Query
- Orden de carga respetando FK
- Ejecución con un solo comando
- Estructura de repositorio organizada

---

## 3. Diseño del Modelo Dimensional (Samuel — 4 min)

### Diálogo sugerido:

> "Para el diseño dimensional seguimos el proceso de 4 pasos:
>
> **Paso 1 — Proceso de Negocio:** Transacciones de venta al por menor, línea por línea.
>
> **Paso 2 — Granularidad:** Cada fila en la tabla de hechos representa una línea de venta individual — un producto, una transacción, un día, una tienda.
>
> **Paso 3 — Dimensiones:** Cinco dimensiones que responden directamente a los requisitos:
> - `DimDate` — Calendario (R1, R2, R5)
> - `DimProduct` — Catálogo de productos (R3, R5)
> - `DimStore` — Tiendas y ubicación (R2, R5)
> - `DimChannel` — Canal de venta (R2)
> - `DimPromotion` — Tipos de promoción (R4)
>
> **Paso 4 — Hechos y Medidas:** La tabla `FactSales` contiene quantity, gross_sales, net_sales, discount_amount, cost_amount, y gross_profit.
>
> Todas las claves surrogate son enteros autoincrementales para garantizar integridad referencial y soportar futuros SCD."

### Mostrar diagrama Star Schema:
- Apuntar al diagrama en el README o en el notebook
- Explicar las relaciones PK/FK
- Justificar que no hay tablas ni atributos innecesarios

### Puntos clave a mencionar:
- Proceso de 4 pasos documentado
- Granularidad: línea de venta
- 5 dimensiones justificadas por requisitos
- Claves surrogate enteras
- Fórmulas de medidas claras

---

## 4. Implementación del Pipeline ETL (Deyton — 4 min)

### Diálogo sugerido:

> "La implementación sigue la arquitectura Extract-Transform-Load:
>
> **Extract:** Leemos `sales_transactions.csv` (1,000 filas) y `reference_data.json` (productos, tiendas, canales, promociones).
>
> **Transform:** Mapeamos IDs naturales a claves surrogate, calculamos las medidas:
> - gross_sales = quantity × list_price
> - net_sales = quantity × unit_price_sale
> - discount_amount = gross_sales − net_sales
> - cost_amount = quantity × unit_cost
> - gross_profit = net_sales − cost_amount
>
> **Load:** Cargamos en orden correcto — dimensiones primero, luego la tabla de hechos, respetando las restricciones FK.
>
> El pipeline completo se ejecuta con `python src/main.py` y genera la base de datos SQLite en `database/retail_dw.db`."

### Mostrar código ejecutando:
```bash
python src/main.py
```

### Puntos clave a mencionar:
- Orden de carga: dimensiones → hechos
- Mapeo de IDs a surrogate keys
- Cálculo de medidas en transform
- Base de datos SQLite con integridad referencial

---

## 5. Queries Analíticos y KPIs (Daniel — 3 min)

### Diálogo sugerido:

> "Implementamos cinco consultas que validan que el modelo soporta los requisitos de negocio:
>
> **R1 — Tendencia mensual de ventas netas:** Agrupamos por mes para identificar períodos de crecimiento o declive.
>
> **R2 — Ventas por tienda y canal:** Comparamos rendimiento entre tiendas físicas y online.
>
> **R3 — Top categorías y marcas:** Identificamos las categorías con mayor ingreso y unidades vendidas.
>
> **R4 — Rendimiento de promociones:** Comparamos ventas, unidades y descuentos por tipo de promoción.
>
> **R5 — Margen bruto por categoría/tienda/mes:** Calculamos ganancia bruta y margen porcentual.
>
> Todas las queries están documentadas en el README y ejecutan correctamente contra el Data Warehouse."

### Puntos clave a mencionar:
- 5 queries = 5 requisitos de negocio
- Queries ejecutan contra dimensiones + hechos
- Resultados impresos en consola
- KPIs calculados correctamente

---

## 6. Visualizaciones y Resultados (Mauricio — 3 min)

### Diálogo sugerido:

> "Generamos dos visualizaciones que confirman los insights del Data Warehouse:
>
> **Visualización 1 — Tendencia Mensual (R1):** Un line chart que muestra la evolución de ventas netas de enero a junio 2026. Permite identificar períodos de crecimiento y declive.
>
> **Visualización 2 — Ventas por Tienda y Canal (R2):** Un bar chart comparativo que muestra el rendimiento de cada tienda/canal. Permite comparar el desempeño relativo.
>
> Ambas visualizaciones se generan desde datos consultados al Data Warehouse, no desde los archivos fuente, lo que valida que el modelo funciona correctamente."

### Mostrar gráficos:
- Abrir las imágenes en `docs/`
- O ejecutar el notebook para mostrarlas en vivo

### Puntos clave a mencionar:
- 2 visualizaciones requeridas
- Datos vienen del Data Warehouse (no fuente)
- Line chart para tendencia temporal
- Bar chart para comparación

---

## 7. Conclusiones y Reflexión (Daniel — 2 min)

### Diálogo sugerido:

> "Para concluir, compartimos tres reflexiones clave:
>
> **Influencia de los requisitos:** Los cinco requisitos de negocio guiaron cada decisión de modelado. Solo creamos dimensiones y hechos que responden directamente a R1-R5. Por ejemplo, `DimPromotion` existe únicamente porque R4 requiere analizar promociones.
>
> **Impacto de una granularidad incorrecta:** Si hubiéramos elegido granularidad a nivel de transacción en lugar de línea de venta, no podríamos analizar productos individuales. Si hubiéramos elegido granularidad diaria aggregada, perderíamos la capacidad de comparar productos o promociones.
>
> **Modelo limpio:** No hay tablas ni atributos innecesarios. Cada elemento está justificado por al menos un requisito de negocio.
>
> El repositorio está limpio, reproducible, y documentado en GitHub."

### Puntos clave a mencionar:
- Requisitos guiaron el modelado
- Granularidad correcta (línea de venta)
- Modelo lean y purpose-driven
- Repositorio reproducible

---

## Preguntas Frecuentes (FAQ)

### "¿Por qué SQLite y no un DW real?"
> SQLite es suficiente para demostrar el modelado dimensional. La arquitectura Star Schema es la misma que se usaría en un DW empresacial (PostgreSQL, Snowflake, etc.).

### "¿Cómo se manejarían cambios lentos en las dimensiones (SCD)?"
> Las claves surrogate enteras permiten implementar SCD Tipo 2 en el futuro, manteniendo historial de cambios.

### "¿Qué pasaría si faltan datos en las fuentes?"
> El pipeline valida que todas las claves existan antes de insertar en FactSales. Las filas con mapeo incompleto se descartan.

### "¿Cómo se escalaría a millones de filas?"
> Se migraría a un DW real (PostgreSQL, Snowflake) y se usaría parallel loading. El diseño dimensional se mantiene igual.

---

## Material de Apoyo

| Archivo | Contenido |
|---------|-----------|
| `README.md` | Documentación completa del proyecto |
| `notebooks/01_dimensional_modeling.ipynb` | Notebook interactivo con modelo + queries + visualizaciones |
| `docs/visualization_monthly_sales.png` | Gráfico de tendencia mensual |
| `docs/visualization_sales_by_store.png` | Gráfico de ventas por tienda |
| `src/main.py` | Pipeline ETL completo |
| `database/retail_dw.db` | Base de datos SQLite generada |

---

## Orden de Ejecución en Presentación

```
1. Mostrar README.md (contexto general)
2. Explicar Arquitectura del Sistema (diagrama de flujo)
3. Explicar diagrama Star Schema
4. Ejecutar: python src/main.py (demo en vivo)
   O: ./scripts/run.sh (Linux/macOS)
   O: scripts\run.bat (Windows)
5. Mostrar resultados en consola (R1-R5)
6. Abrir visualizaciones en docs/
7. Mostrar notebook (opcional, si hay tiempo)
8. Cerrar con reflexión
```

---

> **Tip:** Ejecutar `python src/main.py` o `./scripts/run.sh` antes de la presentación para asegurar que la base de datos esté generada.
