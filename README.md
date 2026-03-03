# iTunes Music Dataset — Business Intelligence Analysis

End-to-end data analysis pipeline on an iTunes music catalog. Goes beyond descriptive stats to extract pricing logic, revenue concentration, catalog segmentation, and actionable business recommendations.

---

## What This Project Does

Most EDA projects describe data. This one interrogates it.

Starting from a raw iTunes track catalog, the pipeline audits data quality, cleans and standardizes the dataset, then answers business questions around pricing structure, revenue concentration, artist catalog dynamics, and market segmentation — delivered as a clean dataset, a reproducible Python script, and a Power BI report.

---

## Key Findings

- **Pricing is binary, not a spectrum.** 78% of tracks sit at the $1.29 iTunes ceiling. There are only two real pricing tiers in this catalog.
- **Revenue follows Pareto.** The top 10% of artists generate 51% of total revenue proxy.
- **The catalog is highly fragmented** (HHI = 42). 2,346 artists across 4,913 tracks — no dominant player.
- **Genre predicts price** more reliably than artist name or track duration.
- **Duration weakly negatively correlates with price** (r = -0.24) — longer tracks trend cheaper, driven by live recordings and classical pieces.

---

## Project Structure

```
iTunes_EDA/
│
├── data/
│   ├── raw/                  # Original dataset (itunes_music_dataset.csv)
│   └── clean/                # Cleaned output (itunes_clean.csv)
│
├── reports/
│   ├── charts/               # Generated visualizations (.png)
│   └── iTunes_BI_Report.pbix # Power BI report (6 pages)
│
├── src/
│   └── config/
│       └── settings.py       # REQUIRED_RAW_COLUMNS and config constants
│
├── main.py                   # Entry point — runs full pipeline
├── itunes_analysis_notebook.py  # Full analysis script (sections 1–9)
├── requirements.py           # Dependencies
└── README.md
```

---

## Pipeline Overview

### 1. Data Audit

- Schema validation against required columns
- Null counts, duplicate detection, type checks
- Price field validation (negative values, zeros, ceiling detection)
- Duration sanity checks (outlier flagging)
- Categorical consistency review (genre, rating, currency)

### 2. Data Cleaning

- Drop rows with missing `artist_name` (not imputable)
- Standardise genre and artist name (strip, title-case)
- Clip negative prices to 0
- Impute missing prices by genre median → global median fallback
- Convert `rating` to boolean `is_explicit` flag
- Impute missing dates by album median → artist median → global median
- Flag duration outliers (`very_short` < 0.5 min, `very_long` > 60 min)
- Deduplicate

### 3–9. Analysis

- Descriptive stats (tracks, artists, genres, price distribution)
- Revenue concentration (Pareto analysis, genre-level revenue)
- Behavioural signals (duration-price correlation, HHI, pricing clusters)
- KMeans segmentation (Budget / Mid-Range / Premium)
- Outlier detection (price, duration, catalog size)
- 6 business-focused visualizations
- Executive summary with 5 insights, 3 risks, 3 recommendations

---

## Visualizations Produced

| Chart                          | Business Question Answered                  |
| ------------------------------ | ------------------------------------------- |
| Price distribution histogram   | Where do prices cluster?                    |
| Genre vs average price         | Which genres command premium pricing?       |
| Top 15 artists by catalog size | Where is catalog concentration?             |
| Revenue proxy by genre         | Where is the money?                         |
| Correlation heatmap            | What actually drives price?                 |
| Price segment scatter          | How do Budget / Mid-Range / Premium differ? |

---

## Power BI Report (6 Pages)

| Page                        | Focus                                                     |
| --------------------------- | --------------------------------------------------------- |
| 1 — Overview                | KPI scorecard, genre tier split, catalog growth over time |
| 2 — Pricing Analysis        | Price distribution, genre pricing, segment matrix         |
| 3 — Revenue Intelligence    | Pareto concentration, genre revenue, artist scatter       |
| 4 — Catalog & Artists       | Top artists, catalog size distribution, HHI               |
| 5 — Segmentation            | Segment scatter, donut share, duration by segment         |
| 6 — Outliers & Data Quality | Duration outliers, large catalogs, assumptions & risks    |

---

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run full pipeline
python main.py
```

Output files will be written to `data/clean/` and `reports/charts/`.

---

## Assumptions

1. **Revenue proxy = unit price per track** — no sales or stream count available. Figures represent pricing potential, not realized revenue.
2. **Negative prices** treated as data entry errors and clipped to $0.
3. **Explicit rate = 0%** is a likely labeling gap in the source data, not a reflection of actual content.
4. **$1.29 price ceiling** is an iTunes platform policy constraint, not organic market pricing.
5. **KMeans k=3** on [unit_price, duration_min] for segmentation — clusters validated against threshold logic.
6. **Missing artist rows dropped** (~0.04% of data) — not imputable without external data.

---

## Tech Stack

- **Python** — pandas, numpy, matplotlib, seaborn, scikit-learn
- **Power BI** — DAX measures, calculated columns, 6-page interactive report
- **Data source** — iTunes music catalog (CSV, 4,915 raw rows)
