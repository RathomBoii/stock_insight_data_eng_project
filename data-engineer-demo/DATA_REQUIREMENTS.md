# Data Requirements — Tech Sector Competitive Benchmarking

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

- **Seasonality** — is there a recurring monthly/quarterly pattern in returns? (e.g., "does this stock tend to be weak in summer?")
- **Year-by-year growth summary** — per-ticker YoY growth, so a user can see the trajectory at a glance.

This is honest, useful, and needs **only price data + fundamentals** — no prediction claims.

### Tier 2 — Decision support (built on top, with guardrails)
The end goal you described: help a user decide **when to buy/sell an individual stock**, and **which stocks are good for the long run**. This sits *on top of* Tier 1 but is a **prediction** product, so it carries extra obligations (backtesting, point-in-time correctness, disclaimers) — see §5/§6.

### How this aligns with the US-vs-China benchmarking goal
They're the **same data, two lenses**, and they compose cleanly:

| | Your seasonal / YoY intent | The benchmarking goal |
|---|---|---|
| **Lens** | Time-series *within* one ticker (when) | Cross-sectional *between* tickers (which) |
| **In the BI** | The metrics (seasonality, YoY growth) | The **slice/group-by** (Cloud/SaaS/Security, US/China) |
| **Data needed** | Price + fundamentals | Price + fundamentals — **identical** |

So the benchmarking isn't a competing project — it's the **filter hierarchy on top of your seasonal/YoY metrics.** "Show me YoY growth *for China Security tickers*" is one dashboard doing both jobs.

### ⚠️ Three data-science caveats baked into these products

1. **"Growth rate" is two different things — we'll show both, and they must not be confused.**
   - *Price growth* (YoY return) — "did the stock go up?" → from your OHLCV alone.
   - *Fundamental growth* (YoY revenue/earnings) — "did the business grow?" → needs `ticker.info` (§2).
   - A stock with great price growth but flat business growth is a warning sign — surfacing that gap is a core Tier-2 signal. **This is another reason fundamentals (§2) are priority #1.**

2. **Seasonality is weak and noisy — 5 years isn't enough to trust it.** ~5 samples per month can't support a confident seasonal claim. So: **please extend the lookback to 10y+** (see §1), and I'll render seasonality with confidence bands, never a bare average line.

3. **A dashboard describes the past; "buy/sell" predicts the future.** The bridge is backtesting under strict point-in-time correctness. Tier 1 charts must not silently become Tier 2 recommendations without that validation — which is exactly why look-ahead bias (§3a, §6) is non-negotiable.

---

## 1. What you've already given me (and it's good)

Your `ingest_stock_price_history.py` lands 5y of OHLCV per ticker, partitioned by `raw/{ticker}/{date}/`.

That already unlocks a lot for me:
- **Daily returns** = `close.pct_change()` → the atomic unit of almost everything I do.
- **Volatility** = rolling std of returns (risk, and a feature for regime detection).
- **Momentum / trend** = moving averages, 52-week high distance.
- **Correlations** = do US and China peers move together or diverge?

### ⚠️ Three things about the price data I need you to lock down

These are the "junior engineer gotchas" that quietly ruin an analysis:

| # | Concern | Why it matters to my models | What I need from you |
|---|---|---|---|
| 1 | **Adjusted vs. raw close** | If a stock splits 2:1, raw price halves overnight — my model sees a fake -50% return. `yfinance` `.history()` returns split/dividend-adjusted prices by default, which is what I want. | Confirm you are **keeping `auto_adjust` behavior**, and keep the `Dividends` + `Stock Splits` columns so I can audit. Don't "clean them away." |
| 2 | **Currency** | US tickers are USD; `0268.HK` is HKD; `300454.SZ` is CNY. I **cannot** compare raw price levels across them. Returns (%) are currency-neutral, but *market cap / valuation* is not. | Carry the **currency** per ticker (comes from `.info`, see §2). I'll convert where needed. |
| 3 | **Trading-calendar misalignment** | US and China exchanges have different holidays. If I naively join on date, I get nulls on days one market was closed. | Just land the raw rows as-is. **Do not forward-fill or invent rows.** I'll align calendars in my feature layer — but I need to know the gaps are *real closures*, not *your ingestion failing*. |
| 4 | **Lookback too short for seasonality** | My seasonal product (see ⭐ section) needs many samples per calendar-month to separate signal from noise. 5y ≈ only 5 samples/month — not enough to trust. | Please bump `LOOKBACK_PERIOD` from `"5y"` to **`"10y"` (or `"max"`)**. It's a one-line change and roughly doubles my statistical power for free. |

That last point is the theme of this whole doc: **I need to be able to tell "the world was quiet" apart from "the pipeline broke."**

---

## 2. Ask #1 — Company fundamentals & profile (`ticker.info`)

**Priority: HIGH.** This is the single highest-value addition. Price tells me *how* a stock moved; fundamentals tell me *whether the business deserves it*.

### What I need
A daily snapshot per ticker of the `ticker.info` fields. In your yfinance version this is assembled from 5 modules — I care about these fields specifically:

| Field group | Fields I'll actually use | What I'll build with it |
|---|---|---|
| **Profile** | `sector`, `industry`, `country`, `currency`, `longName` | Validate your hand-coded `TICKERS.py` grouping against Yahoo's classification; group-level aggregations |
| **Valuation** | `marketCap`, `trailingPE`, `forwardPE`, `priceToBook`, `enterpriseValue` | "Is China SaaS cheaper than US SaaS?" comparisons |
| **Growth & margins** | `revenueGrowth`, `grossMargins`, `operatingMargins`, `profitMargins`, `totalRevenue`, `ebitda` | The core "who's actually winning" fundamental scorecard |
| **Risk** | `beta`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow` | Risk-adjusting my comparisons |
| **Analyst view** | `recommendationKey`, `targetMeanPrice`, `numberOfAnalystOpinions` | Sentiment proxy; a baseline to test my own signals against |

### Engineering notes (the junior-engineer traps)
- **`.info` is a nested dict, not a DataFrame.** Land it as JSON or a one-row parquet. Don't try to force it into the OHLCV schema.
- **It's flaky.** Keys go missing per ticker, and Yahoo rate-limits. **A missing key is normal — do not crash the whole run** because `pegRatio` is absent for one China ticker. Land what you got; leave missing as `null`.
- **It has no timestamp of its own.** `.info` is "right now" with no date attached. **You must stamp your own `ingestion_timestamp`**, or I can't build a time series of fundamentals. This is the most important sentence in this section.
- **Snapshot cadence:** daily is plenty for fundamentals (they update quarterly, but analyst/price-derived fields drift daily). Follow the same `partition by ingestion date` pattern you already built.

---

## 3. Ask #2 — News & sentiment

**Priority: MEDIUM-HIGH.** This is where "context / catalysts" lives. When a stock jumps 8% and I can't explain it from fundamentals, the answer is almost always in the news.

### 3a. Company-specific news
`yfinance` gives you `ticker.news` for free — start there (it's the cheapest path to value).

**What I need per article:** `title`, `publisher`, `link`, `publish_time` (as a real UTC timestamp), and the **ticker it's attached to**.

**What I'll do with it:**
- Run sentiment scoring (title/summary → positive/negative/neutral).
- Build a daily **news volume** feature (a spike in article count often *precedes* a price move).
- **Event study:** align news timestamps to my return series to measure "how much does bad news actually move this stock?"

**⚠️ The critical engineering requirement: timestamps.** Sentiment is only useful if I know *exactly when* the news broke, in a **timezone-normalized (UTC)** field. "Published today" is useless to me. A news item mis-timed by a day will make my event study conclude the opposite of the truth. Please normalize everything to UTC and keep the original timezone in a separate column if you can.

**⚠️ Look-ahead bias (the subtle one).** Never let a news row's `publish_time` be later than the price bar I join it to. If future news leaks into a training row, my backtest looks amazing and then loses money in production. Landing accurate timestamps is how you protect me from this.

### 3b. World / macro news
**Priority: MEDIUM.** Company news explains *idiosyncratic* moves; macro news explains *why the whole sector moved together*.

For our **US-vs-China** thesis specifically, the macro layer is unusually important because of:
- **Regulation** — China tech regulation (antitrust, data-security reviews, VIE-structure risk, US delisting threats). A single policy headline can move every China ticker in our universe at once.
- **Trade / geopolitics** — tariffs, export controls (especially relevant for Security).
- **Rates & FX** — see §4.

I don't need you to solve NLP topic classification. I just need a **raw feed landed** (e.g., a headlines API, RSS, or a licensed source your org already has) with clean timestamps and source. I'll do the filtering. **Starting with a raw, well-timestamped feed beats a fancy pre-filtered one you can't explain.**

---

## 4. Ask #3 — Macro / market context series

**Priority: MEDIUM.** These are the shared "background" variables that let me separate *company* performance from *market* performance.

| Series | Why I need it | Easy source |
|---|---|---|
| **Sector benchmark / index** (e.g., a cloud or software ETF, and a China internet ETF) | To compute **excess return** — did MSFT beat *its market*, or just ride a rising tide? This is the difference between "good company" and "good month." | Just another ticker via your existing pipeline (ETFs work with `yfinance`) |
| **FX rates** (USD/CNY, USD/HKD) | To convert China market caps to USD for apples-to-apples valuation, and because FX *itself* is a driver for cross-listed names | FX pairs are tickers too |
| **Risk-free rate** (e.g., 10Y treasury) | Needed for any risk-adjusted metric (Sharpe ratio, etc.) | FRED or a treasury ticker |
| **Volatility index (VIX)** | Market-wide fear gauge — a strong regime feature | Ticker |

Good news: **these are all just more tickers.** You can likely extend your existing `TICKERS.py` structure with a new top-level group like `"Macro"` rather than building anything new. Reuse beats novelty here.

---

## 5. The data-quality contract (this is non-negotiable, and it's mostly on you)

A model is only as trustworthy as the data under it. Here's what I need *structurally*, regardless of source:

1. **Every record is timestamped in UTC**, with a separate **`ingestion_timestamp`** so I can distinguish "when it happened" from "when we fetched it."
2. **Missing ≠ zero.** A missing fundamental is `null`, not `0`. `0` revenue and *unknown* revenue mean opposite things to a model.
3. **Immutable raw layer.** Never overwrite a partition with "corrected" data — land a new dated partition. I need to reproduce yesterday's model exactly, including yesterday's mistakes. (Your `check_existing_raw_data` skip-if-exists pattern is already the right instinct.)
4. **Freshness signal.** I need to know *when the last successful load ran* per source. A stale feed that silently stops updating is more dangerous than one that loudly fails — it makes my dashboards confidently wrong.
5. **Survivorship bias — flag delistings.** If a China ticker gets delisted and quietly drops out of `TICKERS.py`, my historical analysis will look artificially rosy (only *survivors* remain). If a ticker dies, **keep its history and mark it delisted**; don't just delete it.
6. **Point-in-time correctness.** No field on a given date's record should contain information that wasn't knowable on that date. This is the #1 way data pipelines destroy model validity.

---

## 6. Suggested priority order (so you're not boiling the ocean)

| Order | Deliverable | Effort | My value unlocked |
|---|---|---|---|
| 1 | **`ticker.info` fundamentals** (§2) | Low (yfinance already has it) | High — the whole "who's winning" scorecard |
| 2 | **Macro tickers** (§4: ETFs, FX, VIX) | Low (just more tickers) | High — excess return + currency normalization |
| 3 | **Company news** (§3a) | Medium (timestamp hygiene) | High — explains the moves |
| 4 | **World/macro news feed** (§3b) | Medium-High (new source) | Medium — sector-wide catalysts, China regulation |

**Start with #1 and #2.** They reuse your existing pipeline almost verbatim and unblock the majority of my analysis. News is where the real engineering effort (and payoff) is — tackle it once fundamentals are flowing.

---

## 7. TL;DR for our next standup

- **What we're building:** a **Seasonality + year-by-year growth** BI dashboard, sliceable by our Cloud/SaaS/Security × US/China hierarchy (Tier 1), with buy/sell & long-run **decision support on top** (Tier 2). Your original intent and the benchmarking goal are the **same data, two lenses** — they compose, they don't compete.
- Price data: 👍 — just confirm **adjusted close** and **keep currency**, and **bump lookback `5y` → `10y`** so seasonality is trustworthy.
- Please add **`ticker.info`** next (stamp it with an ingestion timestamp!) — it's also what separates *price growth* from real *business growth*.
- Add **macro tickers** (sector ETF, USD/CNY, USD/HKD, VIX) — they're basically free.
- Then **news with clean UTC timestamps** — this is where you protect me from look-ahead bias.
- The whole thing lives or dies on: **immutable raw, UTC timestamps, missing≠zero, point-in-time correctness.**

Ping me before you design the news schema — I want to make sure the timestamp fields are exactly what my event-study code expects.
