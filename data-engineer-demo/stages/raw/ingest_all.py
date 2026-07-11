import ingest_stock_info
import ingest_stock_ohlc

# Entry point guard: ensures this block runs only when executed directly, not when imported.
# Python sets __name__ = "__main__" when the file is run directly (python ingest_all.py).
# When another file does `import ingest_all`, __name__ = "ingest_all" → this block is skipped.
#
# When to use this guard:
#   ✅ File has top-level code (function calls, loops, I/O) AND is imported by another file.
#   ✅ File is an entry point / orchestrator (best practice even if not imported).
#   ❌ File only defines functions/classes (utils) — no top-level code to protect.
#   ❌ File only holds data/constants (e.g. TICKERS.py) — nothing to run.
if __name__ == "__main__":
    print("=== [1/2] Ingesting stock INFO ===")
    ingest_stock_info.main()

    print("\n=== [2/2] Ingesting stock OHLC ===")
    ingest_stock_ohlc.main()

    print("\n=== Done ===")
