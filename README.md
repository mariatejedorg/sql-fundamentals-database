# 🗄️ SQL Fundamentals Database

> 18 companies, 2 related tables, 4 business questions answered in pure SQL — the second explicit technical skill from the reference job posting (Quant Analyst Sales).

![SQLite](https://img.shields.io/badge/SQLite-database-003B57?logo=sqlite&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-documented%20queries-4479A1?logo=postgresql&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-dashboard-3F4F75?logo=plotly&logoColor=white)

---

## What it does

Loads fundamental data (sector, market cap, P/E ratio, profit margin, revenue growth) for 18 companies into a **SQLite** relational database, along with their recent price history, and answers 4 real business questions with SQL queries — each one documented with its business objective ahead of its code. Unlike the other projects in this portfolio, the focus here isn't the Python analysis but the data model and the SQL itself.

## Dashboard preview

The full interactive version is in [`outputs/dashboard.html`](outputs/dashboard.html): just double-click to open it, no server required. It shows 2 supporting charts and one card per query with its result table.

## Project structure

The first project in this portfolio with a `db/` folder (schema + database) and a `sql/` folder with real, version-controlled `.sql` files — making it clear from the repo alone that this project is, first and foremost, a SQL exercise:

```
sql-fundamentals-database/
├── README.md
├── requirements.txt
├── data/                 <- cached downloaded fundamentals and prices
├── db/
│   ├── schema.sql          <- DDL: table definitions
│   └── fundamentales.db     <- generated SQLite database (not version-controlled)
├── sql/                   <- one query per business question, documented
│   ├── 01_ranking_per_por_sector.sql
│   ├── 02_mejor_margen_por_sector.sql
│   ├── 03_evolucion_metrica_por_sector.sql
│   └── 04_rentabilidad_reciente_por_empresa.sql
├── src/
│   ├── data.py              <- downloads fundamentals and prices (yfinance)
│   ├── build_db.py           <- creates the schema and loads the data into SQLite
│   ├── queries.py             <- runs each .sql via pandas, exposes the business objective
│   ├── dashboard.py            <- interactive dashboard (Plotly) -> outputs/dashboard.html
│   └── main.py                   <- orchestrates the pipeline
└── outputs/               <- generated dashboard
```

## Database schema

```sql
CREATE TABLE empresas (
    ticker TEXT PRIMARY KEY,
    nombre TEXT NOT NULL,
    sector TEXT NOT NULL,
    market_cap REAL,
    per REAL,
    margen_beneficio REAL,
    crecimiento_ingresos REAL
);

CREATE TABLE precios_historicos (
    ticker TEXT NOT NULL,
    fecha TEXT NOT NULL,
    precio_cierre REAL NOT NULL,
    PRIMARY KEY (ticker, fecha),
    FOREIGN KEY (ticker) REFERENCES empresas(ticker)
);
```

`precios_historicos` (price history) exists specifically to enable a **real JOIN** between both tables (query 04) — not just a `GROUP BY` over a flat table, which would be the typical mistake in an overly simple SQL exercise.

## How to run it

```bash
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

On completion, the console prints each query with its business objective and result, and `outputs/dashboard.html` is generated. The database is rebuilt from scratch on every run (`db/fundamentales.db`), from the cache in `data/`.

### A note on SSL certificates
Same mechanism as in the other projects in this portfolio: if `yfinance` fails with `CERTIFICATE_VERIFY_FAILED` (typical with antivirus software that inspects HTTPS traffic, e.g. Norton), `src/data.py` automatically uses a local certificate bundle at `.certs/cacert.pem` if present.

## The 4 queries

| File | Business question | SQL concept |
|---|---|---|
| `01_ranking_per_por_sector.sql` | Which companies trade cheapest (low P/E) within each sector? | `WHERE` (row filtering) + `ORDER BY` |
| `02_mejor_margen_por_sector.sql` | Which company is the most profitable within each sector? | Correlated subquery (`MAX` per sector) |
| `03_evolucion_metrica_por_sector.sql` | Total market cap and average P/E by sector | `GROUP BY` + `AVG`/`SUM` — direct contrast with `WHERE` |
| `04_rentabilidad_reciente_por_empresa.sql` | Each company's recent return, cross-referenced with its P/E | Real `JOIN` between `empresas` and `precios_historicos` |

## Results
_(snapshot as of the run date; 18 companies across 9 sectors)_

- **Technology** is by far the sector with the most weight (≈$9,030B combined market cap) and the most expensive as a group (average P/E of 37.4, vs. 8.7 for Energy) — Apple, Microsoft, SAP and ASML.
- **Repsol** (P/E of 8.7, the lowest in the whole basket) was also the company with the best recent return (+45.3%): a case where "cheap on paper" and "being rewarded by the market" coincided — this isn't always the case, and it's exactly what query 04 lets you check in a single table.
- **LVMH** was the opposite case: mid-range P/E (20.7) but the worst recent return (-16.4%), reflecting the same cooling of the European luxury sector already observed in Market Data Analytics.
- By profit margin, **Microsoft** leads by a wide margin (40.3%) followed by **Banco Santander** (33.5%) — confirming that comparing margins sector by sector (query 02) avoids misleading conclusions: a 33% margin is exceptional in banking but would be mediocre in software.

## Concepts to be able to explain in an interview

- **`WHERE` vs. `GROUP BY`**: `WHERE` filters individual rows *before* any aggregation; `GROUP BY` groups rows into buckets to apply an aggregate function (`AVG`, `SUM`, `COUNT`) to each one — these happen at different moments of query execution, and `HAVING` (not used here, but worth knowing when to reach for) would filter *after* grouping.
- **JOIN**: why cross-referencing `empresas` and `precios_historicos` by `ticker` answers questions neither table can answer on its own — and why this is exactly what a loose CSV can't solve without duplicating data (repeating sector/P/E on every price row, for example).
- **Why a relational database instead of loose CSVs**: referential integrity (`FOREIGN KEY`), avoiding data duplication, and the ability to answer new questions with a query instead of rewriting a pandas script every time.
