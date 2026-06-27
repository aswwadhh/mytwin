#  MyTwin — Personal Academic Analytics Dashboard

> **"See your data. Understand your trajectory. Act on it."**

[![Python](https://img.shields.io/badge/Python-3.11+-blue)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-red)](https://streamlit.io)
[![SQL](https://img.shields.io/badge/Data-SQL%20%2B%20DuckDB-yellow)](https://duckdb.org)
[![dbt](https://img.shields.io/badge/Transform-dbt-orange)](https://getdbt.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

##  Demo

>  **Live Dashboard:** _Coming in Week 4 (Streamlit Cloud)_
>  **Loom Walkthrough:** _Coming in Week 4_

---

##  Problem Statement

**Problem Code:** G1 | **Segment:** Foundations of Analytics Engineering

Students often don't know where they stand academically until it's too late — exam results arrive, CGPA drops, and there's no clear picture of *why* or *what to do next*.

**MyTwin** solves this by turning raw academic data (marks, attendance, assignments) into a personal analytics dashboard. It shows you:
- Where you stand compared to your peers
- How your performance has trended over time
- What your CGPA will be if you score X in your next exam
- What you need to do to match the top performer in your class

Built as part of the **2nd Year B.Tech CSE-AIDE Internship (June–July 2026)** at ScoreLab (fictional edtech company).

---

## Architecture

```
Raw Data (CSV / Spreadsheet)
        │
        ▼
  Data Layer (DuckDB)
  ┌─────────────────────────────┐
  │  fact_academic_events       │
  │  dim_course                 │
  │  dim_time                   │
  │  dim_assignment             │
  │  dim_student                │
  └─────────────────────────────┘
        │
        ▼
  Transformations (dbt / SQL)
  - Cohort comparisons
  - Trend calculations
  - Correlation analysis
  - What-If projections
        │
        ▼
  Dashboard (Streamlit + Plotly)
  ┌────────────────────────────────────┐
  │  Tab 1: My Snapshot                │
  │  Tab 2: Trends                     │
  │  Tab 3: What-If Simulator          │
  │  Tab 4: Peer Benchmarking (Ext.)   │
  └────────────────────────────────────┘
        │
        ▼
  Deployed on Streamlit Cloud (Free)
```

> 📄 Full architecture diagram: [`/docs/architecture.png`](docs/architecture.png) _(coming Week 2)_

---

## 🛠️ Tech Stack

| Component | Choice | Why |
|-----------|--------|-----|
| Language | Python 3.11 | Core language for data work |
| Dashboard | Streamlit | Easiest Python dashboard tool, no frontend needed |
| Charts | Plotly | Interactive charts with minimal code |
| Database | DuckDB | Lightweight, SQL-native, no server needed |
| Transforms | dbt (core) | Clean staging → marts pattern |
| Data format | CSV → SQL | Simple, beginner-friendly |
| Deployment | Streamlit Cloud | Free, 1-click deploy from GitHub |
| Version control | Git + GitHub | Industry standard |

> 📄 Detailed decisions: [`/docs/adr/`](docs/adr/)

---

##  Quickstart

### Prerequisites
- Python 3.11+
- Git
- pip

### Install

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/mytwin.git
cd mytwin

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

### Run

```bash
# Start the dashboard
streamlit run app.py
```

Open your browser at `http://localhost:8501`

### Test

```bash
# Run tests
pytest tests/
```

---

## 📊 Data Sources

| Data | Source | Format |
|------|--------|--------|
| CA Marks | Synthesised| CSV |
| Attendance % | Synthesised | CSV |
| Peer profiles | Manually created (3–4 anonymised) | CSV |

> Raw files are in `/data/raw/`. Transformed files are in `/data/processed/`.

---

##  Folder Structure

```
mytwin/
│
├── app.py                  # Main Streamlit app
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── data/
│   ├── raw/                # Original CSV files
│   └── processed/          # Cleaned, transformed data
│
├── sql/
│   └── sql_portfolio.sql   # 10+ queries with comments
│
├── dbt_project/            # dbt transformations
│   ├── models/
│   │   ├── staging/        # Raw → clean
│   │   └── marts/          # Clean → analytics-ready
│   └── dbt_project.yml
│
├── tests/
│   └── test_transforms.py  # Unit tests
│
└── docs/
    ├── design_doc.md       # 1-page design doc
    ├── insights_memo.md    # 1-page insights brief
    ├── architecture.png    # Architecture diagram
    └── adr/
        ├── ADR-001-dashboard-tool.md
        ├── ADR-002-database-choice.md
        └── ADR-003-data-modelling.md
```

---

## 📈 Dashboard Features

### Tab 1 — My Snapshot
- Overall CGPA and attendance at a glance
- Section rank and batch rank
- Subject-wise marks heatmap
- Subjects needing attention (below average)

### Tab 2 — Trends
- Marks trajectory over weeks/months (line chart)
- Attendance trajectory (area chart)
- Correlation: attendance vs marks (scatter plot)
- Best and worst performing subjects over time

### Tab 3 — What-If Simulator
- Enter a target score for any upcoming exam
- See projected CGPA instantly
- "How many marks do I need to reach 8.0 CGPA?"

### Tab 4 — Peer Benchmarking *(Mini-Extension)*
- Compare yourself against 3 anonymised peer profiles
- Gap analysis: "What do I need to do to match the Top Performer?"
- Visual radar chart of skills vs peers

---

## ➕ Mini-Extension — Peer Benchmarking

**What it is:** A 4th tab that compares your academic profile against 3 created peer profiles — Top Performer, Average Performer, and At-Risk Student.

**What it shows:**
- Side-by-side comparison of marks, attendance, assignment scores
- Gap analysis: exactly what you need to improve to match the top performer
- Radar/spider chart showing strengths and weaknesses

**Why it matters:** This is *prescriptive analytics* — not just "here's what happened" but "here's what to do next." A step above basic descriptive dashboards.

---

##  What I Learned This Week

> _(Updated weekly)_

**Week 1:**
- _To be added after 29 June_

---

## 📄 Documents

| Document | Link |
|----------|------|
| Design Doc | [`docs/design_doc.md`](docs/design_doc.md) |
| Insights Memo | [`docs/insights_memo.md`](docs/insights_memo.md) |
| SQL Portfolio | [`sql/sql_portfolio.sql`](sql/sql_portfolio.sql) |
| ADR-001 | [`docs/adr/ADR-001-dashboard-tool.md`](docs/adr/ADR-001-dashboard-tool.md) |
| ADR-002 | [`docs/adr/ADR-002-database-choice.md`](docs/adr/ADR-002-database-choice.md) |
| ADR-003 | [`docs/adr/ADR-003-data-modelling.md`](docs/adr/ADR-003-data-modelling.md) |
| 3rd Year Roadmap | [`docs/roadmap_3rd_year.md`](docs/roadmap_3rd_year.md) |

---

##  3rd Year Extension Plan

This project is the **seed of a 3rd year portfolio.** Here's where it goes:

| Timeline | What gets added |
|----------|----------------|
| Aug–Sep 2026 | Dropout risk predictor (ML model on current trajectory) |
| Oct–Nov 2026 | Study recommendation engine ("students like you who improved did X") |
| Dec 2026 | Multi-student support (classmates can sign up) |
| Jun–Jul 2027 (3rd year internship) | Full SaaS — multi-tenant, LMS integration, real data |


---

##  Known Limitations

- All data is synthesised — not connected to any real LMS or college system
- What-If simulator uses a simplified CGPA formula
- Peer profiles are manually created, not pulled from a real dataset
- No authentication — this is a personal tool, not multi-user

---

## Resume Bullets

```
• Built MyTwin, a personal academic analytics dashboard using Python,
  SQL, dbt, and Streamlit, deployed on Streamlit Cloud

• Modelled a star-schema warehouse (1 fact table + 4 dimensions) and
  wrote 30+ SQL queries using window functions, CTEs, and aggregations

• Added Peer Benchmarking tab with gap analysis vs top-performer
  profiles — first implementation of prescriptive analytics
```

---

## 👤 About

**Name:** _Aswadh_
**Batch:** B.Tech CSE-AIDE, 2nd Year (2024 batch)
**Internship:** Foundations of Analytics Engineering — Summer 2026
**Problem Code:** G1 — Student Performance Twin

---

##  License

MIT License — see [LICENSE](LICENSE)

---

##  Acknowledgements

- ScoreLab (fictional client scenario) — internship problem framework
- Streamlit, DuckDB, dbt — open-source tools that made this possible
- Internship mentors and cohort — for feedback and support
