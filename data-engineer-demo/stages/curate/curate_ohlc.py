"""Curate stage — clean OHLC using DuckDB SQL.

Reads raw parquet (hive-partitioned), applies data-quality rules and a
daily-return window function, writes a single curated parquet.

Run:
    .venv/bin/python data-engineer-demo/stages/curate/curate_ohlc.py
"""

from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
RAW_GLOB = HERE.parent / "raw" / "raw" / "ohlc" / "**" / "*.parquet"
OUT_DIR = HERE / "curated" / "ohlc"

CURATE_SQL = """
WITH raw AS (
    SELECT
        ticker,
        country,
        industry,
        name,
        Date        AS ts,
        Open        AS open,
        High        AS high,
        Low         AS low,
        Close       AS close,
        Volume      AS volume
    FROM read_parquet($raw_glob, hive_partitioning = 1)
),
valid AS (
    -- data-quality rule: drop malformed bars
    SELECT *
    FROM raw
    WHERE close > 0
      AND high >= low
      AND high >= open AND high >= close
      AND low  <= open AND low  <= close
      AND volume >= 0
),
deduped AS (
    -- one bar per (ticker, day); keep latest if dupes
    SELECT *
    FROM valid
    QUALIFY row_number() OVER (
        PARTITION BY ticker, ts::date
        ORDER BY ts DESC
    ) = 1
)
SELECT
    ticker,
    country,
    industry,
    name,
    ts::date AS trade_date,
    open, high, low, close, volume,
    -- window function: daily simple return vs previous trading day
    close / lag(close) OVER (
        PARTITION BY ticker ORDER BY ts
    ) - 1 AS daily_return
FROM deduped
ORDER BY ticker, trade_date
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_file = OUT_DIR / "curated_ohlc.parquet"

    con = duckdb.connect()
    result = con.execute(CURATE_SQL, {"raw_glob": str(RAW_GLOB)})
    result.df().to_parquet(out_file, index=False)

    n = con.execute(
        "SELECT count(*) FROM read_parquet($f)", {"f": str(out_file)}
    ).fetchone()[0]
    print(f"wrote {n} rows -> {out_file}")


if __name__ == "__main__":
    main()
