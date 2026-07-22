# Stock Insight Data Engineering Project

## Project Overview

This project demonstrates how to build a data pipeline using Python and PySpark that ingests stock market data from Yahoo Finance, stores it in a structured raw layer, and powers a BI dashboard for investment decision support.

---

## Business Requirements

Requirements from business stakeholders:

1. **BI Dashboard** — visualize stock growth in the following perspectives:
   - Seasonality along the year (10-year lookback period)
   - Growth rate by year (10-year lookback period)
2. **Preferred stocks:**
   - US stocks: Cloud, SaaS, Security sectors
   - China stocks: Cloud, SaaS, Security sectors
3. The dashboard should provide insight to help users decide which stocks are the best candidates for long-term investment.

---

## Data Requirements — Tech Sector Competitive Benchmarking

> **From:** Data Science
> **To:** Data Engineering
> **Re:** What I need you to land in the data platform so I can build the "US vs. China Cloud/SaaS/Security" insight product.
> **Audience note:** Written for a junior data engineer. I explain the *why* behind each ask so you can make good trade-offs when the "how" gets messy.

---

## 0. The one-paragraph business goal (read this first)

We want to answer: **"Within Cloud, SaaS, and Security — how do US-listed companies compare to their China-listed peers, and what moves them?"**

That means I need three broad things from you:
1. **Price behavior** — how the stock actually trades over time (returns, volatility, momentum).
2. **Fundamentals** — how the *business* is doing (growth, margins, valuation).
3. **Context / catalysts** — *why* prices move (news, macro, regulation, FX).

You've already delivered #1. This doc scopes #2 and #3, and — importantly — sets the **data-quality contract** so my models don't silently break.

---

## ⭐ The analytical products (what all this data actually feeds)

Before the data asks, here's *what I'm building*, so you can see why each ask exists. There are **two BI products on the same warehouse**, shipped in tiers.

### Tier 1 — Descriptive BI (ships first, low risk)
A dashboard that **describes** each ticker's historical behavior, sliceable by our `industry` / `country` hierarchy:

- **Seasonality** — is there a recurring monthly/quarterly pattern in returns?
- **Year-by-year growth summary** — per-ticker YoY growth, so a user can see the trajectory at a glance.

### Tier 2 — Decision support (built on top, with guardrails)
Help a user decide **when to buy/sell an individual stock**, and **which stocks are good for the long run**. Requires backtesting, point-in-time correctness, and disclaimers.

### How this aligns with the US-vs-China benchmarking goal

| | Your seasonal / YoY intent | The benchmarking goal |
|---|---|---|
| **Lens** | Time-series *within* one ticker (when) | Cross-sectional *between* tickers (which) |
| **In the BI** | The metrics (seasonality, YoY growth) | The **slice/group-by** (Cloud/SaaS/Security, US/China) |
| **Data needed** | Price + fundamentals | Price + fundamentals — **identical** |

### ⚠️ Three data-science caveats

1. **"Growth rate" is two different things** — price growth (YoY return) vs. fundamental growth (YoY revenue/earnings). Both must be shown and must not be confused.
2. **Seasonality is weak with only 5 years** — 10y+ lookback is required for statistical confidence.
3. **A dashboard describes the past; "buy/sell" predicts the future** — Tier 2 requires backtesting under strict point-in-time correctness.

---

## 1. What you've already given me (and it's good)

Your pipeline lands 5y of OHLCV per ticker. That already unlocks daily returns, volatility, momentum, and correlations.

### ⚠️ Three things about the price data to lock down

| # | Concern | What I need |
|---|---|---|
| 1 | **Adjusted vs. raw close** | Confirm `auto_adjust` is on; keep `Dividends` + `Stock Splits` columns |
| 2 | **Currency** | Carry the `currency` field per ticker (from `.info`) |
| 3 | **Trading-calendar misalignment** | Land raw rows as-is — do not forward-fill or invent rows |
| 4 | **Lookback too short** | Bump `LOOKBACK_PERIOD` from `"5y"` to **`"10y"` or `"max"`** |

---

## 2. Ask #1 — Company fundamentals & profile (`ticker.info`)

**Priority: HIGH.**

### Fields needed

| Field group | Fields | What I'll build |
|---|---|---|
| **Profile** | `sector`, `industry`, `country`, `currency`, `longName` | Validate TICKERS.py grouping; group aggregations |
| **Valuation** | `marketCap`, `trailingPE`, `forwardPE`, `priceToBook`, `enterpriseValue` | Cross-country valuation comparison |
| **Growth & margins** | `revenueGrowth`, `grossMargins`, `operatingMargins`, `profitMargins`, `totalRevenue`, `ebitda` | Fundamental scorecard |
| **Risk** | `beta`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow` | Risk-adjusted comparisons |
| **Analyst view** | `recommendationKey`, `targetMeanPrice`, `numberOfAnalystOpinions` | Sentiment proxy |

### Engineering notes
- `.info` is a nested dict — land as JSON or one-row parquet.
- Keys go missing per ticker — do not crash on missing keys; land `null`.
- **You must stamp your own `ingestion_timestamp`** — `.info` has no date of its own.
- Daily snapshot cadence, same partition pattern as OHLCV.

---

## 3. Ask #2 — News & sentiment

**Priority: MEDIUM-HIGH.**

### 3a. Company-specific news
Use `ticker.news` from yfinance. Fields needed per article: `title`, `publisher`, `link`, `publish_time` (UTC), and the ticker it's attached to.

**⚠️ Critical: timestamps must be UTC-normalized.** A news item mis-timed by a day will make an event study conclude the opposite of the truth.

**⚠️ Look-ahead bias:** Never let a news row's `publish_time` be later than the price bar it's joined to.

### 3b. World / macro news
**Priority: MEDIUM.** For the US-vs-China thesis, macro news (regulation, trade, FX, rates) is unusually important. Land a raw, well-timestamped feed — I'll do the filtering.

---

## 4. Ask #3 — Macro / market context series

**Priority: MEDIUM.** These are all just more tickers — extend `TICKERS.py` with a `"Macro"` group.

| Series | Why | Source |
|---|---|---|
| Sector benchmark ETF (cloud, China internet) | Compute excess return | Another yfinance ticker |
| FX rates (USD/CNY, USD/HKD) | Currency normalization | FX pairs are tickers |
| Risk-free rate (10Y treasury) | Sharpe ratio | FRED or treasury ticker |
| VIX | Market-wide fear gauge / regime feature | Ticker |

---

## 5. The data-quality contract (non-negotiable)

1. **Every record is timestamped in UTC** + separate **`ingestion_timestamp`**.
2. **Missing ≠ zero.** A missing fundamental is `null`, not `0`.
3. **Immutable raw layer.** Never overwrite — land a new dated partition.
4. **Freshness signal.** Know when the last successful load ran per source.
5. **Survivorship bias — flag delistings.** Keep delisted ticker history; mark `delisted=True`.
6. **Point-in-time correctness.** No field should contain information not knowable on that date.

---

## 6. Suggested priority order

| Order | Deliverable | Effort | Value unlocked |
|---|---|---|---|
| 1 | **`ticker.info` fundamentals** | Low | High — the "who's winning" scorecard |
| 2 | **Macro tickers** (ETFs, FX, VIX) | Low | High — excess return + currency normalization |
| 3 | **Company news** | Medium | High — explains the moves |
| 4 | **World/macro news feed** | Medium-High | Medium — sector-wide catalysts |

---

## 7. TL;DR

- **Building:** Seasonality + YoY growth BI dashboard (Tier 1), with buy/sell decision support on top (Tier 2).
- Price data ✅ — confirm adjusted close, keep currency, bump lookback to `10y`.
- Next: **`ticker.info`** (stamp with ingestion timestamp).
- Then: **macro tickers** (basically free — more tickers in existing pipeline).
- Then: **news with clean UTC timestamps**.
- Everything depends on: **immutable raw, UTC timestamps, missing≠zero, point-in-time correctness.**
