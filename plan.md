# Project Plan — Lab 2: Dimensional Data Warehouse

> **ETL (G01) — Universidad EAFIT**  
> Sprint: 2026-2-U1-Activity3  
> Duration: 2 weeks (Aug 25 – Sep 7, 2026)

---

## Team

| Name | Role | GitHub |
|------|------|--------|
| Deyton Riascos Ortiz | Project Lead / ETL Developer | [@driosoft-pro](https://github.com/driosoft-pro) |
| Samuel Izquierdo Bonilla | Data Modeling / SQL Developer | [@ZantaCruz](https://github.com/ZantaCruz) |
| Daniel David Garcia Restrepo | Documentation / QA | [@danielrestrepo13](https://github.com/danielrestrepo13) |
| Mauricio Taborda Gongora | Visualization / Testing | [@Taborda004](https://github.com/Taborda004) |

---

## Sprint Backlog

### Sprint 1 — Analysis & Design (Aug 25 – Aug 31)

| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| Read and analyze the lab specification PDF | All | Done | High |
| Create requirements traceability table (Part A) | Samuel | ⬜ To Do | High |
| Define dimensional model: grain, dimensions, facts | Daniel | ⬜ To Do | High |
| Design Star Schema diagram (Part C) | Mauricio | ⬜ To Do | High |
| Set up repository structure and documentation | Deyton | Done | Medium |

**Sprint 1 Deliverable:** Completed traceability table + Star Schema diagram.

---

### Sprint 2 — Implementation (Sep 1 – Sep 7)

| Task | Assignee | Status | Priority |
|------|----------|--------|----------|
| Create schema in SQLite (`create_schema.py`) | Samuel | ⬜ To Do | High |
| Implement dimension loading (`load_dimensions.py`) | Deyton | ⬜ To Do | High |
| Implement fact table loading (`load_fact.py`) | Deyton | ⬜ To Do | High |
| Write SQL queries for R1–R5 (`queries.py`) | Daniel | ⬜ To Do | High |
| Create visualizations (`visualization.py`) | Mauricio | ⬜ To Do | Medium |
| Write `main.py` to orchestrate the pipeline | Deyton | ⬜ To Do | High |
| Test end-to-end pipeline | All | ⬜ To Do | High |
| Update README with final results | Daniel | ⬜ To Do | Medium |

**Sprint 2 Deliverable:** Working Data Warehouse with populated tables and validated queries.

---

## User Stories

### US-01: Requirements Traceability
**As a** team, **we want to** map each business requirement to the required data, expected query, and KPI, **so that** the model is fully traceable.

**Acceptance Criteria:**
- All 5 requirements (R1–R5) are mapped.
- Each requirement has an analytical question, required data, expected query, and KPI.

---

### US-02: Dimensional Model Design
**As a** data engineer, **we want to** design a Star Schema following the 4-step process, **so that** the Data Warehouse is properly structured.

**Acceptance Criteria:**
- Business process is clearly stated.
- Fact table grain is declared in one sentence.
- All 5 dimensions are identified and justified.
- Fact table measures are defined with formulas.
- PK/FK relationships are explicit.

---

### US-03: Star Schema Diagram
**As a** stakeholder, **we want to** visualize the Star Schema, **so that** we can understand the data model at a glance.

**Acceptance Criteria:**
- Diagram shows all tables, keys, measures, and relationships.
- Diagram is created with diagrams.net, Mermaid, or equivalent.

---

### US-04: Data Warehouse Implementation
**As a** developer, **we want to** implement the dimensional model in SQLite, **so that** we can load and query the data.

**Acceptance Criteria:**
- Dimension tables and fact table are created with correct schemas.
- Surrogate keys are auto-increment integers.
- PK and FK constraints are defined.

---

### US-05: Load Pipeline
**As a** developer, **we want to** load data from CSV/JSON into the dimensional model, **so that** the warehouse contains the business data.

**Acceptance Criteria:**
- Source files are read correctly.
- Dimensions are loaded before the fact table.
- Source IDs are mapped to surrogate keys.
- Measures (gross_sales, net_sales, etc.) are calculated.
- FactSales is populated after all dimension keys are available.

---

### US-06: Analytical Validation
**As a** business analyst, **we want to** run SQL queries that prove the model supports R1–R5, **so that** we can trust the Data Warehouse.

**Acceptance Criteria:**
- At least one query per requirement.
- Query results are printed to console.

---

### US-07: Visualizations
**As a** stakeholder, **we want to** see two analytical charts, **so that** we can visually confirm insights from the Data Warehouse.

**Acceptance Criteria:**
- 1 temporal chart (e.g., line chart of monthly sales).
- 1 comparative chart (e.g., bar chart of sales by store).
- Charts use data queried from the Data Warehouse, not raw sources.

---

## Risk Log

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| PDF reader fails to extract text | Medium | Low | Use `pdftotext` CLI as fallback |
| Incorrect grain leads to data loss | High | Medium | Validate grain against each requirement before implementation |
| Surrogate key mapping errors | Medium | Medium | Test mapping with sample rows before full load |
| Missing data in source files | Low | Low | Validate source file completeness during extract |

---

## Definition of Done

- [ ] All 5 business requirements are traceable to model elements.
- [ ] Star Schema is implemented in SQLite with PK/FK constraints.
- [ ] All dimensions and fact table are populated.
- [ ] 5 SQL queries return valid results.
- [ ] 2 visualizations are generated from warehouse data.
- [ ] README is complete with architecture, instructions, and reflections.
- [ ] Repository is clean, reproducible, and pushed to GitHub.

---

## Timeline

```
Week 1 (Aug 25-31)                    Week 2 (Sep 1-7)
┌─────────────────────┐               ┌─────────────────────┐
│ Analysis & Design   │               │ Implementation      │
│                     │               │                     │
│ • Read PDF spec     │               │ • Create schema     │
│ • Traceability tbl  │──────────────►│ • Load pipeline     │
│ • Model design      │               │ • SQL queries       │
│ • Star Schema diagram│              │ • Visualizations    │
│ • Repo structure    │               │ • Testing & QA      │
│                     │               │ • Documentation     │
└─────────────────────┘               └─────────────────────┘
```
