from typing import Final, TypedDict


class TickerRecord(TypedDict):
    industry: str
    country: str
    name: str
    symbol: str
    delisted: bool


# Flat list of ticker records — acts as dim_ticker dimension table.
# Metadata (industry, country) is embedded in each record so it lands in the data,
# not just in the loop. BI tools can join on symbol directly.
TICKERS: Final[list[TickerRecord]] = [
    # --- Cloud Provider / US ---
    {"industry": "Cloud Provider", "country": "US",    "name": "MSFT",       "symbol": "MSFT",      "delisted": False},
    {"industry": "Cloud Provider", "country": "US",    "name": "AMZN",       "symbol": "AMZN",      "delisted": False},
    {"industry": "Cloud Provider", "country": "US",    "name": "GOOGL",      "symbol": "GOOGL",     "delisted": False},
    # --- Cloud Provider / China ---
    {"industry": "Cloud Provider", "country": "China", "name": "BABA",       "symbol": "BABA",      "delisted": False},
    {"industry": "Cloud Provider", "country": "China", "name": "TCEHY",      "symbol": "TCEHY",     "delisted": False},
    {"industry": "Cloud Provider", "country": "China", "name": "KC",         "symbol": "KC",        "delisted": False},
    # --- SaaS / US ---
    {"industry": "SaaS",           "country": "US",    "name": "CRM",        "symbol": "CRM",       "delisted": False},
    {"industry": "SaaS",           "country": "US",    "name": "NOW",        "symbol": "NOW",       "delisted": False},
    {"industry": "SaaS",           "country": "US",    "name": "SNOW",       "symbol": "SNOW",      "delisted": False},
    # --- SaaS / China ---
    {"industry": "SaaS",           "country": "China", "name": "Kingdee",    "symbol": "0268.HK",   "delisted": False},
    {"industry": "SaaS",           "country": "China", "name": "Chinasoft",  "symbol": "0354.HK",   "delisted": False},
    {"industry": "SaaS",           "country": "China", "name": "Weimob",     "symbol": "2013.HK",   "delisted": False},
    # --- Security / US ---
    {"industry": "Security",       "country": "US",    "name": "CRWD",       "symbol": "CRWD",      "delisted": False},
    {"industry": "Security",       "country": "US",    "name": "PANW",       "symbol": "PANW",      "delisted": False},
    {"industry": "Security",       "country": "US",    "name": "FTNT",       "symbol": "FTNT",      "delisted": False},
    # --- Security / China ---
    {"industry": "Security",       "country": "China", "name": "Sangfor",    "symbol": "300454.SZ", "delisted": False},
    {"industry": "Security",       "country": "China", "name": "Venustech",  "symbol": "002439.SZ", "delisted": False},
    {"industry": "Security",       "country": "China", "name": "NSFOCUS",    "symbol": "300369.SZ", "delisted": False},
]