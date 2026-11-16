# E-Commerce ETL Pipeline

An end-to-end ETL pipeline for a fictional online store: raw order and
event CSVs are validated and cleaned with Pandas, loaded into SQLite,
and analysed with SQL aggregations. The pipeline is re-runnable with a
single command and writes a summary report and a chart.

## Skills demonstrated

- Python, Pandas, NumPy, Matplotlib
- SQL (SQLite): schema design, indexes, aggregations, subqueries
- ETL: extract, validate, clean, load
- Data validation: duplicates, missing values, bad dates, invalid quantities
- Reproducible reporting from a single command

## Data

The raw files are **synthetic**: `generate_data.py` builds 1,500 orders
and 4,000 website events for a fictional store, with realistic dirt
injected on purpose (duplicate rows, missing regions, negative
quantities, unparseable dates) so the pipeline has genuine cleaning
work to do. The generation seed is fixed, so the data is reproducible.

## Setup

```bash
pip install -r requirements.txt
```

## How to run

```bash
# 1. Generate the raw data (creates data/raw_orders.csv, data/raw_events.csv)
python generate_data.py

# 2. Run the whole pipeline (creates outputs/ecommerce.db,
#    outputs/REPORT.md, outputs/monthly_revenue.png)
python pipeline.py
```

## Results

From the run in this repo (see `outputs/REPORT.md` for the full report):

- Raw order rows: 1,515 (1,500 generated + 15 injected duplicates)
- Clean orders loaded: 1,481
- Total revenue: $334,668.51
- Average order value: $225.97
- Repeat-customer rate: 85.7%

(The numbers above are from the run in this repo; re-running
`pipeline.py` reproduces them.)

## Project structure

```
ecommerce-etl-pipeline/
├── generate_data.py  # builds the synthetic raw files
├── pipeline.py       # extract, clean, load, query, report
├── queries.sql       # revenue by category, monthly revenue,
│                     # top products, repeat-customer rate
├── data/
│   ├── raw_orders.csv
│   └── raw_events.csv
├── outputs/
│   ├── ecommerce.db         # SQLite database with indexes
│   ├── REPORT.md            # summary report with real run numbers
│   └── monthly_revenue.png  # monthly revenue chart
└── requirements.txt
```
